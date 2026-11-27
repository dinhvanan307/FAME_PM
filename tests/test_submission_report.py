"""Keep the released Word report aligned with the schedule and Pilot 5 evidence."""

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
