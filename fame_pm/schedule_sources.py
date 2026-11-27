"""Re-extract the public FAME cover dates from the pinned PDF inventory."""

import argparse
import csv
import hashlib
import io
import re
from calendar import monthrange
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "evidence/pilot5_esg_pdf_screen.csv"
REGISTER = ROOT / "evidence/deliverables.csv"
# Preserve the five milestone IDs already referenced in the ProjectLibre case study.
HISTORICAL_IDS = {"D1.2": 6, "D2.1": 7, "D4.2": 8, "D6.4": 17, "D6.3": 23}
DATE = r"(\d{4}-\d{2}-\d{2})"


def extract(record, path, uid):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != record["sha256"]:
        raise ValueError(f"PDF fingerprint mismatch: {path}")
    reader = PdfReader(io.BytesIO(data))
    if len(reader.pages) != int(record["pdf_pages"]):
        raise ValueError(f"Page count changed: {path}")
    cover = reader.pages[0].extract_text().replace("\xad", "-")
    report = record["report"]

    def field(pattern):
        hits = re.findall(pattern, cover, re.I | re.M)
        if len(hits) != 1:
            raise ValueError(
                f"{report}: expected exactly one cover field matching {pattern}"
            )
        return hits[0]

    # The D3.4 metadata table suppresses spaces. The display heading retains them.
    heading = field(r"^" + re.escape(report) + r"\s*[-–]\s*([\s\S]+?)\nTitle\s")
    title = " ".join(heading.split())
    version = field(r"^Revision\s*Number\s+(\S+)")
    deadline, month = field(r"^Due\s*Date\s*" + DATE + r"\s*\[Month\s*(\d+)\]")
    delivered = field(r"^Delivered\s*Date\s*" + DATE)
    due, actual = map(date.fromisoformat, (deadline, delivered))
    year = 2023 + (int(month) - 1) // 12
    m = (int(month) - 1) % 12 + 1
    month_end = date(year, m, monthrange(year, m)[1])
    note = ""
    if (due.year, due.month) != (year, m):
        note = (
            f"Hạn ghi ngày và M{month} khác tháng. Nếu lấy cuối M{month} "
            f"({month_end}), sai lệch là {(actual - month_end).days:+d} ngày."
        )
    if report == "D7.2":
        note = (
            "Bản 1.1 nộp lại sau phản biện. Trang 2 ghi bản 1.0 chuẩn bị nộp "
            "ngày 2024-01-15; chưa có biên nhận lần đầu."
        )
    if report == "D6.1":
        note = (
            "D6.4 trang PDF 88 mô tả D6.1 nộp M10 và nộp lại M20. "
            "Số ngày ở đây chỉ áp dụng cho cặp ngày trên bìa D6.1."
        )
    return dict(
        deliverable=report,
        task_uid=uid,
        title=title,
        revision=version,
        due=deadline,
        delivered=delivered,
        variance_days=(actual - due).days,
        due_month=int(month),
        source_url=record["url"] + "#page=1",
        note=note,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT / "du_lieu/schedule")
    parser.add_argument(
        "--download", action="store_true", help="Fetch missing PDFs from FAME"
    )
    parser.add_argument(
        "--write", action="store_true", help="Refresh the verified register"
    )
    args = parser.parse_args()
    with INVENTORY.open(encoding="utf-8", newline="") as src:
        inventory = list(csv.DictReader(src))
    ids = [r["report"] for r in inventory]
    if len(set(ids)) != len(ids) or ids != sorted(ids) or len(ids) != 32:
        raise ValueError(
            "Expected the pinned inventory of 32 distinct, ordered public reports"
        )
    next_uid = 28
    rows = []
    for record in inventory:
        report = record["report"]
        uid = HISTORICAL_IDS.get(report)
        if uid is None:
            uid = next_uid
            next_uid += 1
        path = args.source_dir / (report + ".pdf")
        if args.download and not path.exists():
            with urlopen(
                Request(record["url"], headers={"User-Agent": "FAME-PM/1.0"}),
                timeout=90,
            ) as res:
                data = res.read()
            if hashlib.sha256(data).hexdigest() != record["sha256"]:
                raise ValueError(
                    f"Downloaded PDF differs from the pinned source: {report}"
                )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        rows.append(extract(record, path, uid))
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    if args.write:
        REGISTER.write_text(output.getvalue(), encoding="utf-8")
    elif REGISTER.read_text(encoding="utf-8") != output.getvalue():
        raise ValueError("Published register differs from the PDF covers")
    print(f"Verified {len(rows)} covers against the pinned SHA-256 hashes.")


if __name__ == "__main__":
    main()
