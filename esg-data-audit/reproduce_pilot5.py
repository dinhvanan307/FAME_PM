"""Reproduce numeric ESG exports and a two-profile ranking from FAME Zenodo v1."""
import argparse
import csv
import hashlib
import io
import json
from http.client import IncompleteRead
import time
from pathlib import Path
from urllib.request import urlopen

DOI = "10.5281/zenodo.17175084"
ENDPOINT = "https://zenodo.org/api/records/17175084"
TOL = 1e-8
PILLARS = ("e", "s", "g")


def download(url):
    for attempt in range(3):
        try:
            with urlopen(url, timeout=40) as response:
                return response.read()
        except (OSError, EOFError, IncompleteRead):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def prepare(directory):
    directory.mkdir(parents=True, exist_ok=True)
    metadata_bytes = download(ENDPOINT)
    metadata = json.loads(metadata_bytes)
    for entry in metadata["files"]:
        name = entry["key"]
        if not name.endswith(".csv"):
            continue
        raw = download(f"{ENDPOINT}/files/{name}/content")
        verify(raw, entry)
        (directory / name).write_bytes(raw)
    (directory / "metadata.json").write_bytes(metadata_bytes)


def verify(raw, entry):
    checksum = "md5:" + hashlib.md5(raw).hexdigest()
    if len(raw) != entry["size"] or checksum != entry["checksum"]:
        raise ValueError(f"Unexpected contents of {entry['key']}")


def run(directory):
    record = json.loads((directory / "metadata.json").read_text())
    if record["doi"] != DOI:
        raise ValueError("Wrong Zenodo record")
    entries = record["files"]
    csv_entries = [entry for entry in entries if entry["key"].endswith(".csv")]
    manifest = {}
    tables = {}
    for entry in csv_entries:
        name = entry["key"]
        raw = (directory / name).read_bytes()
        verify(raw, entry)
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
        headers = reader.fieldnames
        if not headers or len(set(headers)) != len(headers):
            raise ValueError(f"Invalid header in {name}")
        rows = []
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"Malformed row in {name}")
            rows.append({k: float(v) if v.strip() else None for k, v in row.items()})
        if not rows:
            raise ValueError(f"Empty table in {name}")
        manifest[name] = {"md5": entry["checksum"], "rows": len(rows), "columns": len(headers)}
        if name.startswith("esgdata_"):
            tables[name.split("_esg", 1)[1].removesuffix(".csv").lstrip("_") or "total"] = rows

    total, adjustment, sectors = tables["total"], tables["adj"], tables["sector_daily"]
    tickers = set(total[0])
    for key, rows in tables.items():
        if len(rows) != len(total):
            raise ValueError(f"Unaligned row count for {key}")
        if key != "sector_daily" and set(rows[0]) != tickers:
            raise ValueError(f"Unexpected ticker set for {key}")

    # Infer one numeric sector series per ticker from the first data row only.
    # The association does not establish an issuer's official industry classification.
    mapping = {}
    for ticker in sorted(tickers):
        implicit_mean = total[0][ticker] - adjustment[0][ticker]
        matches = [s for s, mean in sectors[0].items() if abs(implicit_mean - mean) <= TOL]
        if len(matches) == 1:
            mapping[ticker] = matches[0]

    results = {}
    for pillar in PILLARS:
        checked = matched = baseline_matches = 0
        max_error = 0
        for i in range(1, len(total)):
            for ticker, sector in mapping.items():
                base = tables[pillar][i][ticker]
                expected = tables[pillar + "_adj"][i][ticker]
                estimate = base + total[i][ticker] - sectors[i][sector]
                error = abs(estimate - expected)
                checked += 1
                matched += error <= TOL
                max_error = max(max_error, error)
                baseline_matches += abs(base - expected) <= TOL
        results[pillar] = dict(cells=checked, matched=matched, unchanged_matches=baseline_matches,
                               max_abs_error=max_error)

    # Work on one ordinal row. Scores are ordered before display rounding.
    def ranking(weights):
        def score(ticker):
            values = [round(tables[key][-1][ticker] * 100) for key in PILLARS]
            return sum(v*w for v, w in zip(values, weights))
        ordered = sorted(tickers, key=lambda ticker: (-score(ticker), ticker))
        return ordered, {t: round(score(t) / (100 * sum(weights)), 4) for t in ordered}

    equal, equal_scores = ranking((1, 1, 1))
    green, green_scores = ranking((3, 1, 1))
    ranks = {t: i for i, t in enumerate(equal, 1)}
    alternatives = {t: i for i, t in enumerate(green, 1)}
    sample = max(sorted(tickers), key=lambda t: abs(ranks[t] - alternatives[t]))
    return {
        "doi": DOI, "csv_manifest": manifest, "published_files": len(entries),
        "tolerance": TOL, "calibration_row": 1, "test_rows": [2, len(total)],
        "unique_series_matched": len(mapping), "unmatched_tickers": sorted(tickers - mapping.keys()),
        "held_out": results,
        "ranking_sensitivity": {"row": len(total), "top5_equal": equal[:5], "top5_environment": green[:5],
          "common_top5": len(set(equal[:5]) & set(green[:5])),
          "largest_absolute_rank_change": {"ticker": sample, "equal_rank": ranks[sample],
            "environment_rank": alternatives[sample], "equal_score": equal_scores[sample],
            "environment_score": green_scores[sample]}},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--download", action="store_true", help="Fetch the record metadata and original CSVs before running")
    args = parser.parse_args()
    if args.download:
        prepare(args.data_dir)
    print(json.dumps(run(args.data_dir), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
