"""Inventory the published Zenodo versions, files and actual CSV axes for Pilot 5."""
import argparse
import csv
import json
from pathlib import Path

from reproduce_pilot5 import ENDPOINT, download, load_exports

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results/pilot5_zenodo_inventory.json"


def inventory(data_dir):
    entries, shapes, _ = load_exports(data_dir)
    files = json.loads(download(ENDPOINT + "/files"))["entries"]
    versions = json.loads(download(ENDPOINT + "/versions"))["hits"]
    media = json.loads(download(ENDPOINT + "/media-files"))["entries"]
    if versions["total"] != len(versions["hits"]):
        raise ValueError("Additional version pages require review before publishing the inventory")

    def signatures(items):
        return {r["key"]: (r["checksum"], r["size"]) for r in items}

    if signatures(files) != signatures(entries):
        raise ValueError("Local release metadata differs from the current Zenodo file manifest")
    inventory_files = []
    for item in sorted(files, key=lambda f: f["key"]):
        name = item["key"]
        record = {"file": name, "bytes": item["size"], "checksum": item["checksum"]}
        if name in shapes:
            with (data_dir / name).open(encoding="utf-8-sig", newline="") as source:
                headers = next(csv.reader(source))
            non_tickers = [col for col in headers if not col.endswith(".US")]
            record.update(rows=shapes[name]["rows"], columns=len(headers),
                          ticker_columns=len(headers) - len(non_tickers), other_columns=non_tickers)
        inventory_files.append(record)
    return {
        "record_api": ENDPOINT, "versions_api": ENDPOINT + "/versions",
        "files_api": ENDPOINT + "/files", "media_api": ENDPOINT + "/media-files",
        "version_ids": sorted(item["id"] for item in versions["hits"]),
        "files": inventory_files, "media": sorted(item["key"] for item in media),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "du_lieu/zenodo")
    parser.add_argument("--check", action="store_true", help="Verify the committed inventory against the live API")
    args = parser.parse_args()
    data = inventory(args.data_dir)
    content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if RESULT.read_text(encoding="utf-8") != content:
            parser.exit(1, "The public files, versions or CSV axes have changed; review the evidence.\n")
    else:
        RESULT.write_text(content, encoding="utf-8")
    print(f"{len(data['version_ids'])} version(s), {len(data['files'])} files, "
          f"{sum('rows' in row for row in data['files'])} CSV files, {len(data['media'])} media entries")


if __name__ == "__main__":
    main()
