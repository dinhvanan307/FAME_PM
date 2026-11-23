"""Rebuild condition-level summaries privately. No individual record is returned."""

import csv
from datetime import datetime
from decimal import Decimal
from statistics import median

from .analysis import PASS, OPEN, require, rounded

# Order assigned before the session, identical to the forms distributed.
BLOCKS = {"P1": [("A", (1, 4, 2)), ("B", (5, 3, 6))], "P2": [("B", (4, 2, 1)), ("A", (6, 5, 3))]}
COLUMNS = [
    "Phiếu",
    "Lượt",
    "Cách chấm",
    "KPI",
    "Quyết định",
    "Bắt đầu (UTC)",
    "Kết thúc (UTC)",
    "Thời gian (giây)",
]


def verify_reviews(directory, results):
    key = {r["id"]: r["reference"] for r in results["kpis"]}
    groups = {"A": [], "B": []}
    for person, blocks in BLOCKS.items():
        base = directory / f"FAME_{person}_duyet_nhanh.csv"
        for copy in directory.glob(f"FAME_{person}_duyet_nhanh*.csv"):
            require(copy.read_bytes() == base.read_bytes(), f"Conflicting exports for {person}")
        with base.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream)
            require(next(reader) == COLUMNS, "Unexpected review CSV schema")
            records = list(reader)
        require(len(records) == 6, f"Expected six decisions for {person}")
        previous = None
        for i, row in enumerate(records):
            who, turn, method, kpi, vote, start, end, seconds = row
            label, ids = blocks[i // 3]
            condition = {"Thông thường": "A", "Có gợi ý checklist": "B"}[method]
            require(
                (who, turn, condition, kpi) == (person, str(1 + i // 3), label, f"K{ids[i%3]:02}"),
                "Review row differs from the assigned order",
            )
            require(vote in ("Duyệt", "Không duyệt"), "Invalid vote")
            require(start.endswith("Z") and end.endswith("Z"), "UTC timestamps required")
            start, end = [datetime.fromisoformat(t.replace("Z", "+00:00")) for t in (start, end)]
            elapsed = Decimal(str((end - start).total_seconds()))
            require(
                elapsed == Decimal(seconds)
                and elapsed >= 0
                and (previous is None or start >= previous),
                "Invalid elapsed time or overlapping intervals",
            )
            previous = end
            groups[label].append((kpi, vote == "Duyệt", elapsed))
    for mode, group in groups.items():
        times = [t for _, _, t in group]
        published = results["independent_review"][mode]
        observed = {
            "n": len(group),
            "approvals": sum(v for _, v, _ in group),
            "matches": sum(v == (key[k] == PASS) for k, v, _ in group),
            "false_approvals": sum(v and key[k] == OPEN for k, v, _ in group),
            "total_seconds": rounded(sum(times), 3),
            "median_seconds": rounded(median(times), 6),
        }
        require(
            all(published[k] == v for k, v in observed.items()), f"Aggregate mismatch for {mode}"
        )
