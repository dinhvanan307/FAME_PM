"""Replay the locked Pilot 5 acceptance criteria with decimal arithmetic."""
import argparse
import csv
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "esg-data-audit"
sys.path.insert(0, str(AUDIT))
from reproduce_pilot5 import DOI, PILLARS, verify

FREEZE = "7ac10f303550188d5dce2a6bc5ca2a4f1a7b305c"
CRITERIA = "491b4f18d04d39c5dc9e4b83f871500cd76a8d279e427a1b88ea74a6a35a51b8"
EPS = Decimal("1e-8")


def verify_round(directory):
    if sha256((HERE / "tieu_chi.md").read_bytes()).hexdigest() != CRITERIA:
        raise ValueError("Criteria differ from the frozen version")
    baseline = json.loads((AUDIT / "reproduction.json").read_text())
    record = json.loads((directory / "metadata.json").read_text())
    files = {e["key"]: e for e in record["files"] if e["key"].endswith(".csv")}
    if (record["doi"] != DOI or len(files) != 12 or files.keys() != baseline["csv_manifest"].keys()):
        raise ValueError("Wrong release or incomplete manifest")
    metadata, tables = [], {}
    for name, entry in sorted(files.items()):
        raw = (directory / name).read_bytes()
        verify(raw, entry)
        if entry["checksum"] != baseline["csv_manifest"][name]["md5"]:
            raise ValueError(f"Baseline fingerprint differs for {name}")
        metadata.append({"file": name, "bytes": len(raw), "md5": entry["checksum"]})
        if name.startswith("esgdata_"):
            reader = csv.DictReader(raw.decode("utf-8-sig").splitlines())
            key = name.split("_esg", 1)[1].removesuffix(".csv").lstrip("_") or "total"
            tables[key] = [{k: Decimal(v) for k, v in r.items()} for r in reader]
    total, published, sector = (tables[k] for k in ("total", "adj", "sector_daily"))
    names = set(total[0])
    if len(names) != 100 or len(sector[0]) != 8 or any(len(rows) != 604 for rows in tables.values()):
        raise ValueError("Unexpected release dimensions")
    for key, rows in tables.items():
        headers = set(sector[0]) if key == "sector_daily" else names
        if any(set(r) != headers or not all(v.is_finite() for v in r.values()) for r in rows):
            raise ValueError(f"Invalid numeric panel: {key}")

    means = [sum(r.values()) / len(r) for r in sector]
    ledger = []
    all_matches = base_matches = 0
    largest = Decimal(0)
    for ticker in sorted(names):
        implied = total[0][ticker] - published[0][ticker]
        matches = [s for s, v in sector[0].items() if abs(v - implied) <= EPS]
        if len(matches) == 1:
            reference = [r[matches[0]] for r in sector]
        elif not matches and abs(means[0] - implied) <= EPS:
            reference = means
        else:
            raise ValueError(f"Unresolved or ambiguous: {ticker}")
        pillar_hits = total_hits = fixed_hits = 0
        max_error = Decimal(0)
        for i in range(1, 604):
            shift = total[i][ticker] - reference[i]
            total_hits += abs(shift - published[i][ticker]) <= EPS
            for p in PILLARS:
                raw = tables[p][i][ticker]
                target = tables[p + "_adj"][i][ticker]
                error = abs(raw + shift - target)
                max_error = max(max_error, error)
                pillar_hits += error <= EPS
                if not matches:
                    fixed_hits += abs(raw + total[i][ticker] - means[0] - target) <= EPS
        largest = max(largest, max_error)
        all_matches += pillar_hits
        if matches:
            base_matches += pillar_hits
        else:
            ledger.append({"ticker": ticker, "adjusted_pillars_matched": pillar_hits,
                           "adjusted_total_matched": total_hits, "frozen_reference_matched": fixed_hits,
                           "max_abs_pillar_error": str(max_error.normalize())})
    expected_names = baseline["unmatched_tickers"]
    if ([r["ticker"] for r in ledger] != expected_names or len(ledger) != 9
            or all_matches != 180900 or base_matches != 164619
            or any(r["adjusted_total_matched"] != 603 or r["adjusted_pillars_matched"] != 1809 for r in ledger)):
        raise ValueError("Technical gate failed; inspect references and per-ticker evidence")
    return {"freeze_commit": FREEZE, "criteria_sha256": CRITERIA, "doi": DOI, "files": metadata,
            "absolute_tolerance": str(EPS), "calibration_row": 1, "evaluation_rows": [2, 604],
            "tickers": 100, "baseline_matched": base_matches, "matched": all_matches,
            "denominator": 180900, "max_abs_pillar_error": str(largest.normalize()),
            "additional_pillar_denominator_per_ticker": 1809, "additional_total_denominator_per_ticker": 603,
            "exceptions": ledger}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = verify_round(args.data_dir)
    if args.check:
        if result != json.loads((HERE / "phep_do.json").read_text()):
            raise SystemExit("Replay differs from the published evidence")
        print("Verified 12 source CSVs, 180900 pillar cells and all 9 exception records.")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
