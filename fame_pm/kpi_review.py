"""Load the 25 historically open KPI records and verify the cited public artifacts."""

import argparse
import csv
import hashlib
from io import BytesIO
from pathlib import Path
import re
from urllib.parse import urldefrag
from urllib.request import Request, urlopen
from zipfile import ZipFile

from pypdf import PdfReader

from .portfolio import ROOT

# Open rows in the matrix published at 6c929ea, grouped in review priority order.
BASELINE = {
    3: (1, 2, 3, 4, 5, 8, 9, 10),
    5: (3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 23),
    2: (3, 5),
    4: (2, 6, 7),
    7: (2,),
}
OPEN = "Thiếu bằng chứng"


def records(name):
    with (ROOT / "evidence" / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def read_review():
    refs = records("kpi_review_sources.csv")
    sources = {r["ref"]: r for r in refs}
    if len(sources) != len(refs) or any(
        not r["url"].startswith("https://")
        or not re.fullmatch(r"[0-9a-f]{64}", r["sha256"])
        for r in refs
    ):
        raise ValueError("Invalid review source catalogue")
    rows = records("kpi_review.csv")
    ids = [f"P{p}-{n:02d}" for p, numbers in BASELINE.items() for n in numbers]
    if [r["id"] for r in rows] != ids:
        raise ValueError("Review must cover the exact 25 open records at 6c929ea")
    for i, r in enumerate(rows, 1):
        if r["before"] != OPEN or not all(r.values()) or r["ref1"] == r["ref2"]:
            raise ValueError(f"Incomplete review: {r['id']}")
        r["order"] = i
        r["sources"] = [sources[r[k]] for k in ("ref1", "ref2")]
    return {r["id"]: r for r in rows}


def compact(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


def verify_files(directory, download):
    refs = records("kpi_review_sources.csv")
    by_file = {}
    for record in refs:
        by_file.setdefault(record["filename"], []).append(record)
    for name, entries in by_file.items():
        path = directory / name
        url, _ = urldefrag(entries[0]["url"])
        if name == "quality_assessment.py":
            url = url.replace("github.com", "raw.githubusercontent.com").replace(
                "/blob/", "/"
            )
        fetch = download and not path.exists()
        if fetch:
            request = Request(
                url, headers={"User-Agent": "FAME-PM course evidence audit"}
            )
            with urlopen(request, timeout=120) as response:
                data = response.read()
        else:
            data = path.read_bytes()
        checksum = hashlib.sha256(data).hexdigest()
        if any(r["sha256"] != checksum for r in entries):
            raise ValueError(f"Changed source: {name}")
        if fetch:
            directory.mkdir(exist_ok=True, parents=True)
            path.write_bytes(data)
        if name.endswith(".pdf"):
            pages = PdfReader(BytesIO(data)).pages
        for r in entries:
            if name.endswith(".pdf"):
                index = int(r["url"].split("#page=")[1]) - 1
                match = compact(r["anchor"]) in compact(pages[index].extract_text())
            elif name.endswith(".zip"):
                with ZipFile(BytesIO(data)) as archive:
                    match = r["anchor"] in archive.namelist()
            else:
                match = r["anchor"].encode() in data
            if not match:
                raise ValueError(f"Anchor missing for {r['ref']}: {r['anchor']}")
        if name == "d63.pdf":
            users = compact(pages[51].extract_text())
            rankings = compact(pages[52].extract_text())
            checks = (
                (
                    users,
                    r"viewersusersesgrankingtablescount20users5rankings[a-z]+28viewersuserscompare",
                ),
                (
                    users,
                    r"viewersuserscompareesgrankingtablescount20users5rankings[a-z]+25viewersusersoftrainings",
                ),
                (
                    rankings,
                    r"esgrankingtablesuploadedcomparednumberofesgtabularrecommendationscomparedcount3[a-z]+9portfolioweightings",
                ),
            )
            if not all(re.search(pattern, page) for page, pattern in checks):
                raise ValueError(
                    "Cannot locate the 28 viewers, 25 comparison users and 9 ESG rankings in D6.3"
                )
        if name == "D1.4.pdf":
            # Test all nine separately named ranking assets, excluding portfolio weights.
            span = " ".join(p.extract_text() for p in pages[46:57])
            titles = re.findall(
                r"Table\s+(\d+)\s*[–-]\s*Ranking\s+(Aggressive|Balanced|Conservative)",
                span,
            )
            if [int(number) for number, _ in titles] != list(range(27, 36)):
                raise ValueError(
                    "Cannot locate all nine ranking tables on PDF pp. 47–57"
                )
        print(f"{name}: {len(entries)} reference(s) verified")
    print(f"{len(by_file)} files and {len(refs)} source references verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    read_review()
    verify_files(args.source_dir, args.download)
