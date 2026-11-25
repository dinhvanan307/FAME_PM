"""Verify the evidence matrix, its public workbook and the linked KPI pages."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import unicodedata

from .kpi_review import read_review
from .open23_register import attach_runs
from .pilot_evaluation import page_url, read_evaluation
from .portfolio import ROOT, SOURCES, BASE, pages

COUNTS = (5, 8, 10, 7, 23, 8, 4)
STATUSES = ("Đạt", "Không đạt", "Thiếu bằng chứng", "Không áp dụng theo FAME")
BOOK = ROOT / "FAME_Ma_tran_65_KPI.xlsx"
COLUMNS = (
    "id",
    "pilot",
    "kpi",
    "target",
    "actual",
    "assessment",
    "rationale",
    "period",
    "target_pages",
    "actual_pages",
    "period_url",
    "supporting_url",
    "source_name",
    "legacy_id",
)
LEGACY = {
    "P5-21": "K01",
    "P5-14": "K02",
    "P5-01": "K03",
    "P5-07": "K04",
    "P5-23": "K05",
    "P5-10": "K06",
}


def read_matrix():
    with (ROOT / "evidence/kpi_matrix.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    ids = [
        f"P{pilot}-{i:02d}"
        for pilot, count in enumerate(COUNTS, 1)
        for i in range(1, count + 1)
    ]
    if [r["id"] for r in rows] != ids or len(
        {(r["pilot"], r["source_name"]) for r in rows}
    ) != sum(COUNTS):
        raise ValueError("Duplicate, missing or misordered KPI")
    for r in rows:
        if any(
            not value
            for key, value in r.items()
            if key not in {"legacy_id", "supporting_url"}
        ):
            raise ValueError(f"Incomplete record: {r['id']}")
        if r["assessment"] not in STATUSES or r["id"].split("-")[0] != "P" + r["pilot"]:
            raise ValueError(f"Invalid decision or pilot: {r['id']}")
        if r["legacy_id"] != LEGACY.get(r["id"], ""):
            raise ValueError(f"Wrong six-KPI cross-reference: {r['id']}")
        for name, doc in (("target", "d64"), ("actual", "d63")):
            pp = r[name + "_pages"].split("–")
            if (
                len(pp) > 2
                or not all(x.isdigit() for x in pp)
                or int(pp[-1]) < int(pp[0])
            ):
                raise ValueError(f"Invalid page range: {r['id']}")
            if r[name + "_url"] != BASE + SOURCES[doc][0] + "#page=" + pp[0]:
                raise ValueError(f"Incorrect page link: {r['id']}")
        for key, doc in (("period_url", "d63"), ("supporting_url", "d62")):
            if r[key] and not re.fullmatch(
                re.escape(BASE + SOURCES[doc][0]) + r"#page=[1-9]\d*", r[key]
            ):
                raise ValueError(f"Wrong source: {r['id']} {key}")
    legacy_rows = json.loads(
        (ROOT / "results/pm_results.json").read_text(encoding="utf-8")
    )["kpis"]
    legacy = {r["id"]: r for r in legacy_rows}
    for r in rows:
        if r["legacy_id"]:
            old = legacy[r["legacy_id"]]
            if (r["assessment"], r["target_url"], r["actual_url"]) != (
                old["decision"],
                old["target_source"],
                old["observation_source"],
            ):
                raise ValueError(f"Conflict with the six-KPI case: {r['id']}")
    review = read_review()
    for r in rows:
        r["review"] = review.get(r["id"])
        if r["review"] and r["review"]["after"] != r["assessment"]:
            raise ValueError(f"Review decision and matrix disagree: {r['id']}")
    return attach_runs(rows)


def normalized(text):
    return re.sub("[^a-z0-9]", "", unicodedata.normalize("NFKD", text).lower())


def verify_sources(rows, directory):
    texts = {
        doc: [normalized(pg) for pg in pages(directory, doc, False)] for doc in SOURCES
    }
    for r in rows:
        anchor = normalized(r["source_name"])[:24]
        for key, doc in (("target", "d64"), ("actual", "d63")):
            first, *rest = map(int, r[key + "_pages"].split("–"))
            last = rest[0] if rest else first
            if last > len(texts[doc]) or anchor not in texts[doc][first - 1]:
                raise ValueError(
                    f"Cannot locate {r['id']} in {doc} on PDF page {first}"
                )
        for key, doc, anchor_text in (
            ("period_url", "d63", "phase2"),
            ("supporting_url", "d62", "pilot3"),
        ):
            if r[key]:
                page = int(r[key].split("#page=")[1])
                if key == "supporting_url" and page == 33:
                    anchor_text = "amazonwebservices"
                if anchor_text not in texts[doc][page - 1]:
                    raise ValueError(f"Source context missing: {r['id']} {key}")


def verify_workbook(rows):
    from openpyxl import load_workbook

    book = load_workbook(BOOK)
    sheet = book["Ma tran"]
    if sheet.max_row != len(rows) + 1 or not sheet.tables or not sheet.freeze_panes:
        raise ValueError("Workbook row count, filter or frozen header is missing")
    for row_num, row in enumerate(rows, 2):
        for col, key in enumerate(COLUMNS, 1):
            cell = sheet.cell(row_num, col)
            if key in ("target_pages", "actual_pages", "period_url", "supporting_url"):
                url = row[
                    {"target_pages": "target_url", "actual_pages": "actual_url"}.get(
                        key, key
                    )
                ]
                if not url and cell.value in (None, "—"):
                    continue
                if not cell.hyperlink or cell.hyperlink.target != url:
                    raise ValueError(f"Incorrect Excel hyperlink: {cell.coordinate}")
                if url:
                    doc, locator = {
                        "target_pages": ("D6.4", row["target_pages"]),
                        "actual_pages": ("D6.3", row["actual_pages"]),
                        "period_url": ("D6.3", url.split("#page=")[1]),
                        "supporting_url": ("D6.2", url.split("#page=")[1]),
                    }[key]
                    if cell.value != f"{doc} · {locator}":
                        raise ValueError(
                            f"Incorrect Excel source label: {cell.coordinate}"
                        )
            elif str(cell.value or "") != row[key]:
                raise ValueError(f"Excel differs at {cell.coordinate} for {row['id']}")
    detail = book["Ra soat 25 KPI"]
    reviewed = sorted(
        (r for r in rows if r["review"]), key=lambda r: r["review"]["order"]
    )
    if (
        detail.max_row != len(reviewed) + 1
        or not detail.tables
        or not detail.freeze_panes
    ):
        raise ValueError("Review worksheet is incomplete")
    for i, row in enumerate(reviewed, 2):
        r = row["review"]
        values = (
            row["id"],
            row["kpi"],
            row["target"],
            row["period"],
            r["before"],
            row["assessment"],
            r["finding"],
            r["resolution"],
            *(s["label"] for s in r["sources"]),
        )
        if tuple(detail.cell(i, j).value for j in range(1, 11)) != values:
            raise ValueError(f"Review worksheet differs for {row['id']}")
        for j, source in enumerate(r["sources"], 9):
            link = detail.cell(i, j).hyperlink
            if not link or link.target != source["url"]:
                raise ValueError(f"Wrong review hyperlink at {i}, {j}")
    execution = book["Kiem thu 23 KPI"]
    cases = sorted(
        (r for r in rows if r.get("execution")), key=lambda r: r["execution"]["order"]
    )
    if (
        execution.max_row != len(cases) + 1
        or not execution.tables
        or not execution.freeze_panes
    ):
        raise ValueError("Invalid 23-KPI worksheet")
    for i, row in enumerate(cases, 2):
        case = row["execution"]
        expected = [
            row["id"],
            row["kpi"],
            row["target"],
            row["period"],
            case["method"],
            case["observation"],
            row["assessment"],
            case["owner"],
            case["request"],
            case["decision_rule"],
        ]
        if [execution.cell(i, j).value for j in range(1, 11)] != expected:
            raise ValueError(f"Execution worksheet differs for {row['id']}")
        for j, url in ((11, case["url"]), (12, row["target_url"])):
            link = execution.cell(i, j).hyperlink
            if not link or link.target != url:
                raise ValueError(f"Execution link differs for {row['id']}")
    cached = load_workbook(BOOK, data_only=True)
    pentagon = book["Innovation Pentagon"]
    data, means = read_evaluation()
    if [c.value for c in pentagon[1][1:6]] != data["dimensions"]:
        raise ValueError("Innovation Pentagon dimension order differs")
    for i, figure in enumerate([*data["pilots"], data["portfolio"]], 2):
        expected_name = f"Pilot {figure['pilot']}" if "pilot" in figure else "FAME công bố"
        expected_scores = list(map(float, figure["scores"]))
        source = pentagon[f"G{i}"]
        if ([c.value for c in pentagon[i][:6]] != [expected_name, *expected_scores]
                or source.value != f"Hình {figure['figure']} · tr. PDF {figure['page']}"
                or not source.hyperlink or source.hyperlink.target != page_url("d63", figure["page"])):
            raise ValueError(f"Innovation Pentagon differs at figure {figure['figure']}")
    for col, mean in zip("BCDEF", means):
        if (pentagon[col+"10"].value != f"=ROUND(AVERAGE({col}2:{col}8),2)"
                or pentagon[col+"11"].value != f"={col}10-{col}9"
                or cached[pentagon.title][col+"10"].value != float(mean)
                or cached[pentagon.title][col+"11"].value != 0):
            raise ValueError(f"Wrong Innovation Pentagon reconciliation in {col}")
    summary = cached["Tong hop"]
    profiles = next(r["execution"]["profiles"] for r in cases if r["id"] == "P5-13")
    for i, percent in enumerate((0, 25, 50, 75, 100), 28):
        expected = [
            percent / 100,
            *(
                p["rows_changing_top5_members_vs_equal"]
                for p in profiles
                if p["weight_percent"] == percent
            ),
        ]
        if [summary.cell(i, j).value for j in range(1, 5)] != expected:
            raise ValueError("Incorrect five-level ESG grid in workbook")
    for i in range(1, 8):
        counts = Counter(r["assessment"] for r in rows if int(r["pilot"]) == i)
        expected = [i, COUNTS[i - 1], *(counts[k] for k in STATUSES)]
        if [summary.cell(5 + i, j).value for j in range(1, 7)] != expected:
            raise ValueError(f"Wrong Excel totals for pilot {i}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--source-dir", type=Path, help="Directory of the three pinned FAME PDFs"
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Print the validated rows for artifact builders",
    )
    args = p.parse_args()
    rows = read_matrix()
    if args.json:
        print(json.dumps(rows, ensure_ascii=False))
        return
    verify_workbook(rows)
    if args.source_dir:
        verify_sources(rows, args.source_dir)
    print(
        f"Verified {len(rows)} rows in CSV and Excel: {dict(Counter(r['assessment'] for r in rows))}"
    )
    if args.source_dir:
        print("Verified PDF fingerprints, KPI name anchors and page references.")


if __name__ == "__main__":
    main()
