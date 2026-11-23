"""Replay publicly testable parts of the 23 KPI dossiers open at commit 2ee5042."""

import argparse
import csv
from decimal import Decimal
from hashlib import md5, sha256
import json
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZipFile

from pypdf import PdfReader

from .kpi_review import records
from .portfolio import ROOT
from .sensitivity import order_scores

RESULT = ROOT / "results/open23_runs.json"


def upstream_inputs(directory):
    by_name = {r["filename"]: r["sha256"] for r in records("kpi_review_sources.csv")}
    files = {}
    for name in (
        "fdac.zip",
        "FAME-integration.zip",
        "d62.pdf",
        "d63.pdf",
        "fame_presentation.pdf",
    ):
        path = directory / name
        if sha256(path.read_bytes()).hexdigest() != by_name[name]:
            raise ValueError(f"Unexpected upstream source: {name}")
        files[name] = path
    return files


def pdf_page(path, number):
    return " ".join(PdfReader(path).pages[number - 1].extract_text().split())


def package_member(archive, suffix):
    (name,) = [n for n in archive.namelist() if n.endswith("/" + suffix)]
    return archive.read(name)


def catalogue(files, node):
    with ZipFile(files["fdac.zip"]) as archive, tempfile.TemporaryDirectory() as tmp:
        module = Path(tmp) / "catalogue.mts"
        spec = Path(tmp) / "swagger.json"
        module.write_bytes(package_member(archive, "services/iot-catalogue-service.ts"))
        spec.write_bytes(package_member(archive, "swagger.json"))
        run = subprocess.run(
            [node, str(ROOT / "fame_pm/fdac_replay.mjs"), str(module), str(spec)],
            check=True,
            text=True,
            capture_output=True,
        )
        replay = json.loads(run.stdout)
        api = json.loads(spec.read_bytes())
    operations = sorted(
        f"{method.upper()} {path}"
        for path, desc in api["paths"].items()
        for method in desc
        if method in {"get", "post", "put", "patch", "delete"}
    )
    with ZipFile(files["FAME-integration.zip"]) as archive:
        objects = {}
        for name in archive.namelist():
            if "/fdac-open-api/" not in name or not name.endswith(".yaml"):
                continue
            text = archive.read(name).decode()
            kind = re.search(r"(?m)^kind:\s*(\w+)", text)[1]
            item = {"file": name.rsplit("/", 1)[-1]}
            if kind == "Deployment":
                item["replicas"] = int(re.search(r"(?m)^  replicas:\s*(\d+)", text)[1])
            objects[kind] = item
    text = pdf_page(files["d62.pdf"], 31)
    use_cases = re.findall(r"UC([12])\s*[–-]\s*(.+?):\s*This use case", text)
    if [n for n, _ in use_cases] != ["1", "2"]:
        raise ValueError("Cannot identify both use cases in D6.2 p.31")
    return dict(
        use_cases=dict(use_cases),
        operations=operations,
        schema_names=sorted(api["components"]["schemas"]),
        manifests=objects,
        replay=replay,
    )


def originals(directory):
    manifest = json.loads((ROOT / "esg-data-audit/reproduction.json").read_text())[
        "csv_manifest"
    ]
    tables = {}
    digests = {}
    for suffix in ("_esg", "_esg_e", "_esg_s", "_esg_g", "_ms_daily", "_close_full"):
        (name,) = [n for n in manifest if n.endswith(suffix + ".csv")]
        raw = (directory / name).read_bytes()
        checksum = "md5:" + md5(raw).hexdigest()
        if checksum != manifest[name]["md5"]:
            raise ValueError(f"Unverified original CSV: {name}")
        digests[name] = checksum
        data = list(csv.reader(raw.decode("utf-8-sig").splitlines()))
        header, *rows = data
        if len(set(header)) != len(header) or any(
            len(row) != len(header) for row in rows
        ):
            raise ValueError(f"Invalid original CSV dimensions: {name}")
        tables[suffix] = (header, rows)
    return tables, digests


def weighting_trials(tables):
    headers, records_e = tables["_esg_e"]
    data = [tables["_esg_" + pillar] for pillar in "esg"]
    if any(head != headers or len(rows) != len(records_e) for head, rows in data):
        raise ValueError("Unaligned pillar rows or tickers")

    # Integer hundredths preserve the source precision and exact ranking ties.
    def cents(value):
        scaled = Decimal(value) * 100
        if not scaled.is_finite() or int(scaled) != scaled or not 0 <= scaled <= 10000:
            raise ValueError(f"Invalid pillar score: {value}")
        return int(scaled)

    panels = [[[cents(v) for v in row] for row in rows] for _, rows in data]
    # Ignore repeated identical panels only for sorting, preserving every row in counts.
    cache = {}
    profiles = []
    for axis, pillar in enumerate("ESG"):
        for percent in (0, 25, 50, 75, 100):
            weights = [100 - percent] * 3
            weights[axis] = 2 * percent  # denominator 200; remainder split equally
            changed = 0
            for row in zip(*panels):
                key = tuple(tuple(v) for v in row)
                if key not in cache:
                    cache[key] = {}
                rankings = cache[key]
                for profile in (tuple(weights), (1, 1, 1)):
                    if profile not in rankings:
                        scored = {
                            ticker: sum(p * v for p, v in zip(profile, values))
                            for ticker, values in zip(headers, zip(*row))
                        }
                        rankings[profile] = tuple(order_scores(scored)[:5])
                trial = rankings[tuple(weights)]
                changed += set(trial) != set(rankings[(1, 1, 1)])
            profiles.append(
                {
                    "pillar": pillar,
                    "weight_percent": percent,
                    "weights_percent": [v / 2 for v in weights],
                    "rows_changing_top5_members_vs_equal": changed,
                    "last_row_top5": list(trial),
                }
            )
    return {
        "ordinal_rows": len(records_e),
        "tickers": len(headers),
        "profiles": profiles,
        "unique_input_panels": len(cache),
        "ranking_tie_break": "ticker ascending",
    }


def backtest(pdf):
    text = pdf_page(pdf, 24).split("Short Period", 1)[1].split("Sources:", 1)[0]
    results = {}
    for label in ("Balanced blend", "ESG only", "Sharpe optimizer"):
        pattern = (
            re.escape(label) + r"\s+[\d.]+\s+[\d.]+\s+([\d.]+)%\s+([\d.]+)\s+([\d.]+)%"
        )
        match = re.search(pattern, text)
        if not match:
            raise ValueError(f"Missing one-year MS023 row: {label}")
        roi, sharpe, mdd = map(Decimal, match.groups())
        results[label] = {
            "return_pct": float(roi),
            "sharpe": float(sharpe),
            "max_drawdown_pct": float(mdd),
        }
    for label in ("Balanced blend", "ESG only"):
        for key in ("return_pct", "max_drawdown_pct"):
            results[label][key + "_delta_pp"] = round(
                results[label][key] - results["Sharpe optimizer"][key], 2
            )
    return results


def run(source_dir, data_dir, node):
    files = upstream_inputs(source_dir)
    tables, digests = originals(data_dir)
    tickers, scores = tables["_esg"]
    signals, signal_rows = tables["_ms_daily"]
    prices, price_rows = tables["_close_full"]
    if not all(re.fullmatch(r"[A-Z0-9.\-]+\.US", k) for k in signals + prices):
        raise ValueError("Reassess date keys in these CSV headers")
    final = {k: Decimal(v) for k, v in zip(tickers, scores[-1])}
    p4 = pdf_page(files["d63.pdf"], 44)
    # D6.3 table 4 includes both counts on the imported-records row.
    return dict(
        baseline="2ee504207ad4c5aae6f5b213d02503c11e0f0732",
        csv_md5=digests,
        pilot3=catalogue(files, node),
        pilot5={
            "weights": weighting_trials(tables),
            "scores": {
                "rows": len(scores),
                "tickers": len(tickers),
                "nonempty_cells": sum(bool(v) for row in scores for v in row),
                "last_row_min": float(min(final.values())),
                "last_row_max": float(max(final.values())),
            },
            "join": {
                "signal_rows": len(signal_rows),
                "price_rows": len(price_rows),
                "common_tickers": len(set(signals) & set(prices)),
                "signal_tickers": len(signals),
                "price_tickers": len(prices),
                "missing_signal_cells": sum(not v for row in signal_rows for v in row),
                "explicit_dates": False,
                "correlation": None,
            },
            "ms023_one_year": backtest(files["fame_presentation.pdf"]),
        },
        pilot4=import_counts(p4),
    )


def import_counts(text):
    match = re.search(
        r"Database Entries.*?enriched analysis\. (\d+) (\d+) Processing Speed",
        text,
        flags=re.I,
    )
    if not match:
        raise ValueError("Cannot locate the P4 before/after counts in D6.3")
    before, after = map(int, match.groups())
    return {"before": before, "after": after, "delta_records": after - before}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--node", default="node", help="Node.js 24+")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run(args.source_dir, args.data_dir, args.node)
    if args.check:
        if json.loads(RESULT.read_text()) != result:
            raise SystemExit("Replay differs from the published results.")
        print(
            "Verified original FDAC examples, all ESG weight trials, data join checks and reported aggregates."
        )
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
