"""Populate Chapter 5 from the student's risk register, issue log and KPI evidence."""

import csv
from pathlib import Path

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.table import Table

from report.kpi_appendix import source_link, td

EVIDENCE = Path(__file__).resolve().parents[1] / "evidence"


def records(name):
    with (EVIDENCE / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def caption_table(doc, anchor):
    (caption,) = doc.element.body.xpath(f"./w:p[w:bookmarkStart[@w:name='{anchor}']]")
    node = caption.getprevious()
    if node.tag != qn("w:tbl") or len(node.findall(qn("w:tr"))) != 1:
        raise ValueError(f"Expected a header-only table before {anchor}")
    return Table(node, doc)


def fill_risk_chapter(doc, kpis):
    risks = records("risk_register.csv")
    issues = records("risk_issues.csv")
    risk_ids = {r["risk_id"] for r in risks}
    if len(risk_ids) != len(risks) or len({r["issue_id"] for r in issues}) != len(
        issues
    ):
        raise ValueError("Duplicate risk or issue identifier")
    if any(r["risk_id"] not in risk_ids for r in issues):
        raise ValueError("Issue refers to an unregistered risk")

    register = caption_table(doc, "t77")
    matrix = caption_table(doc, "risk_rank_table")
    scores = {}
    for risk in risks:
        risk_id = risk["risk_id"]
        code, situation, action = register.add_row().cells
        td(code, risk_id, bold=True)
        td(code, risk["category"], second=True)
        p = td(situation, risk["risk"] + " " + risk["signal"] + " ")
        source_link(p, risk["source_label"], risk["source_url"])
        p = td(action, risk["owner"] + ". ", bold=True)
        p.add_run(risk["response"]).font.size = Pt(10.5)
        if risk["p"] or risk["i"]:
            prob, impact = int(risk["p"]), int(risk["i"])
            if not (1 <= prob <= 3 and 1 <= impact <= 3):
                raise ValueError(f"Rating out of range for {risk_id}")
            scores.setdefault((prob, impact), []).append(risk_id)

    log = caption_table(doc, "t80")
    for issue in issues:
        code, observation, disposition = log.add_row().cells
        td(code, issue["risk_id"], bold=True)
        td(code, issue["issue_id"], second=True)
        td(observation, issue["origin"] + ". " + issue["observed"])
        p = td(disposition, issue["disposition"] + " ")
        source_link(p, issue["evidence_label"], issue["evidence_url"])

    for impact in (3, 2, 1):
        label, *cells = matrix.add_row().cells
        td(label, f"I = {impact}", bold=True)
        for prob, cell in enumerate(cells, 1):
            score = impact * prob
            level = "cao" if score >= 6 else "vừa" if score >= 3 else "thấp"
            shading = OxmlElement("w:shd")
            shading.set(
                qn("w:fill"),
                {"thấp": "E8F2EA", "vừa": "FCF0D4", "cao": "F8E1DC"}[level],
            )
            cell._tc.get_or_add_tcPr().append(shading)
            td(cell, f"{score} · {level}")
            assigned = scores.get((prob, impact))
            if assigned:
                td(cell, ", ".join(assigned), second=True, bold=True)

    follow_up = caption_table(doc, "risk_kpi_follow_up")
    for kpi in kpis:
        if kpi["decision"] != "Thiếu bằng chứng":
            continue
        key, owner, evidence = follow_up.add_row().cells
        td(key, kpi["id"], bold=True)
        td(key, kpi["label"], second=True)
        td(owner, kpi["proposed_owner_b"])
        p = td(evidence, kpi["requested_evidence"] + " ")
        source_link(p, "Ngưỡng", kpi["target_source"])
        p.add_run(" · ")
        source_link(p, "Kết quả FAME", kpi["observation_source"])
