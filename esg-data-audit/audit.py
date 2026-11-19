"""Audit two original FAME/MarketSenseAI exports using only Python's standard library."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen

RECORD = "https://zenodo.org/api/records/17175084"
FILES = {
    "esg": (
        "esgdata_2022-12-31_2025-06-01_45391872bed3f263_esg.csv",
        "fb61411b6b6af42d4bde72cb5fa89eef",
    ),
    "signals": (
        "marketsense_2022-12-31_2025-06-01_f2fc372c98cd70e8_ms_daily.csv",
        "aa155da7820c19b58325aeb8ddba598e",
    ),
}


def inspect(filename, checksum, directory):
    if directory is None:
        with urlopen(f"{RECORD}/files/{filename}/content", timeout=30) as response:
            raw = response.read()
    else:
        raw = (directory / filename).read_bytes()
    if hashlib.md5(raw).hexdigest() != checksum:
        raise ValueError(f"{filename}: checksum differs from Zenodo record 17175084")
    reader = csv.reader(io.StringIO(raw.decode("utf-8-sig")))
    headers = next(reader)
    tickers = {name for name in headers if name.endswith(".US")}
    rows = blanks = 0
    for row in reader:
        if len(row) != len(headers):
            raise ValueError(f"{filename}: inconsistent column count at line {reader.line_num}")
        rows += 1
        blanks += sum(not cell.strip() for cell in row)
    return {
        "rows": rows,
        "columns": len(headers),
        "unique_us_tickers": len(tickers),
        "non_ticker_headers": [name for name in headers if name not in tickers],
        "blank_cells": blanks,
    }, tickers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, help="Read the two original CSVs from this directory")
    args = parser.parse_args()
    summary, symbols = {}, {}
    for label, (filename, checksum) in FILES.items():
        summary[label], symbols[label] = inspect(filename, checksum, args.data_dir)
    summary["common_us_tickers"] = len(symbols["esg"] & symbols["signals"])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
