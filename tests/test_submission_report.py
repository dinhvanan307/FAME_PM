"""Keep the released Word report aligned with the schedule and Pilot 5 evidence."""

import csv
import json
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def text(element):
    return "".join(t.text or "" for t in element.iter(W + "t"))


class SubmissionReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with ZipFile(ROOT / "FAME_Bao_cao_cuoi_ky.docx") as file:
            cls.body = ET.fromstring(file.read("word/document.xml")).find(W + "body")

    def test_risks_link_register_issues_priorities_and_kpi_evidence(self):
        def table_before(anchor):
            body = list(self.body)
            caption = next(i for i, p in enumerate(body)
                           if p.find(f"{W}bookmarkStart[@{W}name='{anchor}']") is not None)
            table = body[caption - 1]
            self.assertEqual(table.tag, W + "tbl")
            return [[text(c) for c in row.findall(W + "tc")]
                    for row in table.findall(W + "tr")[1:]]

        def evidence(name):
            with (ROOT / "evidence" / name).open(encoding="utf-8", newline="") as source:
                return list(csv.DictReader(source))

        risks = evidence("risk_register.csv")
        issues = evidence("risk_issues.csv")
        self.assertEqual([row[0] for row in table_before("t77")],
                         [r["risk_id"] + r["category"] for r in risks])
        self.assertEqual([row[0] for row in table_before("t80")],
                         [r["risk_id"] + r["issue_id"] for r in issues])
        self.assertEqual({r["issue_id"] for r in issues if r["risk_id"] == "RR-04"},
                         {"VD-04", "VD-05"})
        matrix = table_before("risk_rank_table")
        for risk in risks:
            if risk["p"]:
                cell = matrix[3 - int(risk["i"])][int(risk["p"])]
                self.assertIn(risk["risk_id"], cell)
                self.assertTrue(cell.startswith(str(int(risk["i"]) * int(risk["p"]))))
        data = json.loads((ROOT / "results/pm_results.json").read_text())
        open_kpis = [k for k in data["kpis"] if k["decision"] == "Thiếu bằng chứng"]
        rows = table_before("risk_kpi_follow_up")
        self.assertEqual([row[:2] for row in rows],
                         [[k["id"] + k["label"], k["proposed_owner_b"]] for k in open_kpis])
        for row, k in zip(rows, open_kpis):
            self.assertIn(k["requested_evidence"], row[2])

    def test_work_package_summary_uses_entire_schedule(self):
        schedule = json.loads((ROOT / "results/pm_results.json").read_text())[
            "schedule"
        ]
        expected = [
            ["Gói công việc", "Số báo cáo", "Giao sớm", "Đúng ngày", "Giao trễ"]
        ]
        rows = schedule["deliverables"]
        for number in range(1, 8):
            days = [
                r["variance_days"]
                for r in rows
                if r["deliverable"].startswith(f"D{number}.")
            ]
            expected.append(
                [
                    f"WP{number}",
                    str(len(days)),
                    str(sum(d < 0 for d in days)),
                    str(days.count(0)),
                    str(sum(d > 0 for d in days)),
                ]
            )
        expected.append(
            [
                "Toàn bộ",
                str(len(rows)),
                str(schedule["early"]),
                str(schedule["on_deadline"]),
                str(schedule["late"]),
            ]
        )
        tables = [
            t
            for t in self.body.findall(W + "tbl")
            if text(t.find(W + "tr").find(W + "tc")) == expected[0][0]
        ]
        self.assertIn(
            expected,
            [
                [
                    [text(c) for c in row.findall(W + "tc")]
                    for row in t.findall(W + "tr")
                ]
                for t in tables
            ],
        )

    def test_conclusion_keeps_both_esg_rounds_and_appendix_links_resolve(self):
        pm = json.loads((ROOT / "results/pm_results.json").read_text())
        confirmed = json.loads((ROOT / "Pilot5_nghiem_thu/phep_do.json").read_text())
        conclusion = next(
            text(p)
            for p in self.body.findall(W + "p")
            if text(p).startswith("Kết luận thực nghiệm của người viết.")
        )
        self.assertIn(f"{pm['esg']['tickers']} mã", conclusion)
        self.assertIn(f"{confirmed['tickers']} mã", conclusion)
        cells = f"{confirmed['matched']:,}/{confirmed['denominator']:,}".replace(
            ",", "."
        )
        self.assertIn(cells, conclusion)
        for letter in "ABCDEFGHIJKL":
            anchor = f"FameAppendix{letter}"
            matches = self.body.findall(f".//{W}hyperlink[@{W}anchor='{anchor}']")
            self.assertEqual([text(link) for link in matches], [f"Phụ lục {letter}"])
            targets = [
                text(p)
                for p in self.body.findall(W + "p")
                if p.find(f"{W}bookmarkStart[@{W}name='{anchor}']") is not None
            ]
            self.assertEqual(len(targets), 1)
            self.assertRegex(targets[0], rf"^(?:Phụ lục )?{letter}[ .]")
