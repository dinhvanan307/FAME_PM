"""Index the seven FAME pilots directly from the pinned D6.2, D6.3 and D6.4 PDFs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.fame-horizon.eu/wp-content/uploads/"
SOURCES = {
    "d62": ("2025/05/FAME-D6.2-_-Integrated-Pilot-Systems-and-Pilot-Operations.pdf",
            "756dfdeb1954f80a90e5a62211862d1e8655c49c6b4a7386ebe2014e5d86c6a6"),
    "d63": ("2025/05/FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf",
            "c84810db23c1bbae3f980da26771193a1f7125c02543d6d7d7584531d70b0a5b"),
    "d64": ("2026/02/FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf",
            "85153ef591b23c4b15316ee0ac88b83b44a47b534af244946c2292742862256d"),
}


def pages(directory, name, download):
    path = directory / (name + ".pdf")
    url, expected = SOURCES[name]
    fetch = download and not path.is_file()
    if fetch:
        with urllib.request.urlopen(BASE + url, timeout=60) as response:
            data = response.read()
    else:
        data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"{name}: unexpected PDF fingerprint")
    if fetch:
        directory.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return [p.extract_text() for p in PdfReader(io.BytesIO(data)).pages]


def page_of(document, pattern):
    matches = [i for i, page in enumerate(document, 1) if re.search(pattern, page, re.M)]
    if len(matches) != 1:
        raise ValueError(f"Expected one body page for {pattern!r}, found {matches}")
    return matches[0]


def portfolio(directory, download=False):
    operations, evaluation, specification = [pages(directory, name, download) for name in SOURCES]
    summary = page_of(specification, r"^Table 1\s*[–-]\s*Pilots Summary\s*$")
    annex = page_of(specification, r"^\s*Annex A Business Requirements\s*[–-]\s*Co-Creation Workshop\s*$")
    chunks = re.split(r"(?m)^Pilot #(\d+) (\w+) ", specification[summary - 1])[1:]
    pilots = []
    for number, lead, content in zip(chunks[::3], chunks[1::3], chunks[2::3]):
        n = int(number)
        uses = [int(i) for i in re.findall(r"•\s*UC\s*#(\d+)", content)]
        if not uses or uses != list(range(1, len(uses) + 1)):
            raise ValueError(f"Unexpected use-case numbering for pilot {n}")
        requirements = {}
        for i, page in enumerate(specification[annex - 1:], annex):
            for req in re.findall(rf"\bP{n}_BR\d+\b", page):
                requirements.setdefault(req, []).append(i)
        pilots.append(dict(
            pilot=n, lead=lead, use_cases=uses, annex_identifiers=requirements,
            operations_pdf_page=page_of(operations, rf"^3\.{n}\s+Pilot\s*#{n} [^.\n]*(?:\.(?!\.))?\s*$"),
            target_table_pdf_page=page_of(specification, rf"^Table \d+\s*[–-]\s*Pilot {n}: KPIs\s*$"),
            outcome_table_end_pdf_page=page_of(evaluation, rf"^Table {n}: Pilot {n} KPI\s*$"),
        ))
    if [p["pilot"] for p in pilots] != list(range(1, 8)):
        raise ValueError("Missing or duplicate pilot in D6.4 Table 1")
    return dict(
        sources={k: {"url": BASE + v[0], "sha256": v[1]} for k, v in SOURCES.items()},
        summary_pdf_page=summary, annex_pdf_page=annex,
        total_use_cases=sum(len(p["use_cases"]) for p in pilots),
        total_distinct_annex_identifiers=sum(len(p["annex_identifiers"]) for p in pilots),
        pilots=pilots,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True, help="Folder for d62.pdf, d63.pdf and d64.pdf")
    parser.add_argument("--download", action="store_true", help="Fetch missing pinned PDFs")
    parser.add_argument("--check", action="store_true", help="Compare the new index with the committed result")
    args = parser.parse_args()
    index = portfolio(args.data_dir, args.download)
    if args.check:
        expected = json.loads((ROOT / "results/pilot_portfolio.json").read_text())
        if index != expected:
            raise SystemExit("Pilot index differs from the published result")
        print(f"Verified {len(index['pilots'])} pilots and {index['total_use_cases']} use cases from three PDFs")
    else:
        print(json.dumps(index, indent=2))


if __name__ == "__main__":
    main()
