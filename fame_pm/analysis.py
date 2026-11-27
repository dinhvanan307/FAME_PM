"""Calculate PM indicators. Excel is read only as a published evidence record."""

import csv
import json
from collections import Counter
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from statistics import median
from xml.etree import ElementTree

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
PASS, FAIL, OPEN = "Đạt", "Không đạt", "Thiếu bằng chứng"
SPEC = (
    "https://www.fame-horizon.eu/wp-content/uploads/2026/02/"
    "FAME-D6.4-Use-Cases-Specification-and-Pilot-Sites-Preparation.-II.pdf"
)
EVAL = (
    "https://www.fame-horizon.eu/wp-content/uploads/2025/05/"
    "FAME-D6.3-Techno-Economic-Evaluation-and-Stakeholders-Feedback.pdf"
)
# Physical PDF page numbers, including the cover. Printed pages are four lower.
PAGES = {
    "K01": (71, 54),
    "K02": (70, 53),
    "K03": (69, 52),
    "K04": (70, 52),
    "K05": (71, 54),
    "K06": (70, 53),
}


def rounded(value, places):
    return float(Decimal(str(value)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_schedule(root, cordis):
    with (root / "evidence/deliverables.csv").open(encoding="utf-8", newline="") as stream:
        records = list(csv.DictReader(stream))
    tree = ElementTree.parse(root / "FAME_Lich_MS_Project.xml")
    ns = {"p": "http://schemas.microsoft.com/project"}
    tasks = {t.findtext("p:UID", namespaces=ns): t for t in tree.findall("p:Tasks/p:Task", ns)}

    def day(uid, field):
        raw = tasks[uid].findtext(field, namespaces=ns)
        require(raw, f"Missing {field} on Project task {uid}")
        return date.fromisoformat(raw.split("T")[0])

    baseline_ids = {u for u, t in tasks.items() if t.find("p:Baseline", ns) is not None}
    require({r["task_uid"] for r in records} == baseline_ids, "Baseline set differs from covers")
    require(
        len(records) == len({r["deliverable"] for r in records}) == len(baseline_ids) == 32,
        "Expected 32 distinct covers and milestone IDs",
    )
    result = []
    for record in records:
        uid = record["task_uid"]
        due = date.fromisoformat(record["due"])
        delivered = date.fromisoformat(record["delivered"])
        require(
            tasks[uid].findtext("p:Name", namespaces=ns).startswith(record["deliverable"] + " |"),
            f"Task name does not match {record['deliverable']}",
        )
        require(
            (due, delivered) == (day(uid, "p:Baseline/p:Finish"), day(uid, "p:ActualFinish")),
            f"Cover and Project calendar differ for {record['deliverable']}",
        )
        variance = (delivered - due).days
        require(due == day(uid, "p:Deadline") and int(record["variance_days"]) == variance
                and tasks[uid].findtext("p:HyperlinkAddress", namespaces=ns) == record["source_url"],
                f"Cover deadline, source or variance mismatch for {record['deliverable']}")
        result.append({**record, "variance_days": variance})
    case = next(row for row in result if row["deliverable"] == "D6.4")
    review = day("15", "p:ActualFinish")
    require(review.isoformat() == "2025-02-03", "D6.4 review differs from revision 0.6")
    before = (review - date.fromisoformat(case["due"])).days
    after = (date.fromisoformat(case["delivered"]) - review).days
    rp2 = [day("24", "p:Start").isoformat(), day("24", "p:Finish").isoformat()]
    require(
        rp2
        == cordis["rp2"]
        == [day("25", "p:ActualFinish").isoformat(), day("26", "p:ActualFinish").isoformat()],
        "RP2 mismatch",
    )
    days = [row["variance_days"] for row in result]
    by_wp = {}
    for row in result:
        wp = "WP" + row["deliverable"].split(".")[0][1:]
        by_wp.setdefault(wp, []).append(row["variance_days"])
    without_notes = [row["variance_days"] for row in result if not row["note"]]
    return {
        "deliverables": result,
        "by_work_package": {wp: {"reports": len(values), "late": sum(d > 0 for d in values)}
                            for wp, values in by_wp.items()},
        "excluding_annotated_covers": {
            "reports": len(without_notes),
            "late": sum(d > 0 for d in without_notes),
            "median_signed_days": median(without_notes),
        },
        "late": sum(d > 0 for d in days),
        "early": sum(d < 0 for d in days),
        "on_deadline": days.count(0),
        "on_time": sum(d <= 0 for d in days),
        "median_signed_days": median(days),
        "d64_before_review_days": before,
        "d64_after_review_days": after,
        "rp2": rp2,
    }


def assess(direction, threshold, observation, value, unit, measured_unit, comparable):
    """A bound only proves a verdict when its entire interval is on one side of the gate."""
    require(direction in ("<=", ">="), f"Unsupported threshold {direction}")
    if value is None or not comparable or unit != measured_unit:
        return OPEN
    require(observation in ("Giá trị", "<", "<=", ">", ">="), f"Unknown observation {observation}")
    threshold, value = Decimal(str(threshold)), Decimal(str(value))
    if observation == "Giá trị":
        meets = value <= threshold if direction == "<=" else value >= threshold
        return PASS if meets else FAIL
    if observation in ("<", "<="):
        if direction == "<=" and value <= threshold:
            return PASS
        if direction == ">=" and (value < threshold or (value == threshold and observation == "<")):
            return FAIL
    if observation in (">", ">="):
        if direction == ">=" and value >= threshold:
            return PASS
        if direction == "<=" and (value > threshold or (value == threshold and observation == ">")):
            return FAIL
    return OPEN


def kpi_results(book):
    results = []
    for n, cells in enumerate(
        book["Nguon_KPI"].iter_rows(min_row=5, max_row=10, values_only=True), 5
    ):
        (
            key,
            label,
            direction,
            threshold,
            unit,
            kind,
            value,
            measured_unit,
            description,
            scope,
            _,
            _,
            ok,
        ) = cells
        baseline = book["Ho_so_A"][n]
        checklist = book["Checklist_B"][n]
        require(key == baseline[0].value == checklist[0].value, f"KPI ID mismatch at row {n}")
        require(ok in (0, 1), f"Invalid scope flag for {key}")
        decision = assess(direction, threshold, kind, value, unit, measured_unit, bool(ok))
        reference = baseline[5].value
        require(
            checklist[6].value == decision and checklist[7].value == reference,
            f"Independent rule and archived workbook disagree for {key}",
        )
        spec_page, eval_page = PAGES[key]
        results.append(
            dict(
                id=key,
                label=label,
                direction=direction,
                threshold=threshold,
                unit=unit,
                observation_type=kind,
                observed=value,
                observed_unit=measured_unit,
                project_description=description,
                scope=scope,
                comparable=bool(ok),
                decision=decision,
                reference=reference,
                baseline=baseline[3].value,
                owner_a=baseline[4].value,
                proposed_owner_b=checklist[8].value,
                requested_evidence=checklist[9].value,
                target_source=f"{SPEC}#page={spec_page}",
                observation_source=f"{EVAL}#page={eval_page}",
            )
        )
    require({r["id"] for r in results} == set(PAGES), "Six unique KPI records required")
    retro = {}
    for condition, verdict, owner in [
        ("A", "baseline", "owner_a"),
        ("B", "decision", "proposed_owner_b"),
    ]:
        retro[condition] = dict(
            matches=sum(r[verdict] == r["reference"] for r in results),
            open=sum(r[verdict] == OPEN for r in results),
            with_owner=sum(bool(r[owner]) and r[verdict] == OPEN for r in results),
        )
    return results, retro


def public_review(root, kpis):
    path = root / "Cham_doc_lap/Ket_qua/Tong_hop_A_B.xlsx"
    book = load_workbook(path, data_only=True, read_only=True)
    try:
        rows = list(book["Tong_hop"].values)
    finally:
        book.close()
    require(
        [r[0] for r in rows[4:12]]
        == [
            "Số lượt chấm",
            "Số quyết định Duyệt",
            "Số quyết định khớp tham chiếu",
            "Tỷ lệ khớp",
            "Duyệt khi thiếu bằng chứng",
            "Tổng số giây",
            "Trung bình (giây/KPI)",
            "Trung vị (giây/KPI)",
        ],
        "Aggregate sheet layout changed",
    )
    result = {}
    for index, condition in [(1, "A"), (2, "B")]:
        n, approved, matches, rate, false_pass, total, cached_mean, med = [
            row[index] for row in rows[4:12]
        ]
        classes = Counter(r["reference"] for r in kpis)
        require(
            n == len(kpis)
            and 0 <= false_pass <= classes[OPEN]
            and 0 <= matches <= n
            and 0 <= approved <= n
            and total > 0
            and med >= 0,
            "Invalid review totals",
        )
        require(
            abs(matches / n - rate) < 1e-10 and abs(total / n - cached_mean) < 1e-10,
            "Cached A/B sums disagree",
        )
        result[condition] = dict(
            n=n,
            approvals=approved,
            matches=matches,
            accuracy_pct=100 * matches / n,
            false_approvals=false_pass,
            missing_evidence_cases=classes[OPEN],
            total_seconds=rounded(total, 3),
            mean_seconds=rounded(total / n, 6),
            median_seconds=rounded(med, 6),
        )
    result["delta_mean_seconds"] = rounded(
        result["B"]["mean_seconds"] - result["A"]["mean_seconds"], 3
    )
    result["delta_median_seconds"] = rounded(
        Decimal(str(result["B"]["median_seconds"])) - Decimal(str(result["A"]["median_seconds"])), 4
    )
    return result


def funding(cordis):
    rows = []
    for name, cost, eu in cordis["funding"]:
        total, grant = Decimal(cost), Decimal(eu)
        require(0 <= grant <= total and total > 0, f"Invalid CORDIS amount for {name}")
        rows.append(
            dict(
                name=name,
                cost_eur=cost,
                eu_eur=eu,
                other_eur=str(total - grant),
                eu_share_pct=rounded(grant * 100 / total, 2),
            )
        )
    return rows


def pm_results(root=ROOT):
    cordis = json.loads((root / "evidence/cordis.json").read_text(encoding="utf-8"))
    book = load_workbook(root / "FAME_Nghiem_thu_6_KPI.xlsx", data_only=True)
    try:
        kpis, retro = kpi_results(book)
    finally:
        book.close()
    return dict(
        grant=cordis["grant"],
        schedule=read_schedule(root, cordis),
        funding=funding(cordis),
        kpis=kpis,
        retrospective=retro,
        independent_review=public_review(root, kpis),
    )
