"""Use temporary, synthetic ballots to exercise the release and reconciliation rules."""
import json
import tempfile
import unittest
from datetime import datetime, timedelta
from importlib.util import find_spec
from pathlib import Path
from unittest.mock import patch

from openpyxl import load_workbook

from Pilot5_nghiem_thu.tong_hop import HERE, SPEC, report_review, summarize


def example_ballots(folder):
    paths = {}
    for person in ("P1", "P2"):
        book = load_workbook(HERE / f"{person}.xlsx")
        paths[person] = folder / f"{person}.xlsx"
        start = datetime(2000, 1, 1, 9)
        for index, (mode, cases) in enumerate(SPEC[person], 1):
            sheet = book[f"Luot {index}"]
            for n, key in enumerate(cases, 6):
                finish = start + timedelta(seconds=20 if mode == "B" else 30)
                sheet[f"E{n}"], sheet[f"F{n}"] = start, finish
                start = finish
                approve = key in {"R1", "R3", "R5"} or (person == "P1" and key == "R2")
                sheet[f"H{n}"] = "Duyệt" if approve else "Không duyệt"
                sheet[f"I{n}"] = "Giá trị mô phỏng cho kiểm thử."
                if mode == "B":
                    for col in "JKL":
                        sheet[f"{col}{n}"] = "Có"
        book.save(paths[person])
        book.close()
    return paths


class ReviewRoundTests(unittest.TestCase):
    def test_published_templates_are_empty_and_valid(self):
        result = summarize(HERE / "P1.xlsx", HERE / "P2.xlsx")
        self.assertEqual((result["received_complete_ballots"], result["valid_decisions"]), (0, 0))
        self.assertIsNone(result["comparison"])

    def test_reject_swapped_ballots(self):
        with self.assertRaisesRegex(ValueError, "danh tính"):
            summarize(HERE / "P2.xlsx", HERE / "P1.xlsx")

    def test_comparison_requires_two_complete_ballots(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = example_ballots(Path(temp))
            self.assertIsNone(summarize(paths["P1"], HERE / "P2.xlsx")["comparison"])
            complete = summarize(paths["P1"], paths["P2"])
            self.assertEqual(complete["disagreement_ids"], ["R2"])
            self.assertEqual(complete["agreements"], 5)
            self.assertEqual(complete["comparison"]["A"]["false_approvals"], 1)
            self.assertEqual(complete["comparison"]["B"]["reference_positive"], 3)
            self.assertEqual(complete["comparison"]["B"]["median_seconds"], 20)
            book = load_workbook(paths["P1"])
            book["Luot 1"]["E6"] = "=NOW()"
            book.save(paths["P1"])
            book.close()
            with self.assertRaisesRegex(ValueError, "tĩnh"):
                summarize(paths["P1"], paths["P2"])

    def test_report_updates_from_returns_and_replays_aggregate(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            snapshot = folder / "released.json"
            blank = summarize(HERE / "P1.xlsx", HERE / "P2.xlsx")
            snapshot.write_text(json.dumps(blank))
            paths = example_ballots(folder)
            pending = folder / "awaiting-P2.xlsx"
            paths["P2"].rename(pending)
            with (patch("Pilot5_nghiem_thu.tong_hop.PRIVATE_BALLOTS", folder),
                  patch("Pilot5_nghiem_thu.tong_hop.PUBLIC_RESULT", snapshot)):
                one = report_review()
                self.assertEqual((one["received_complete_ballots"], one["valid_decisions"]), (1, 6))
                self.assertIsNone(one["comparison"])
                pending.rename(paths["P2"])
                both = report_review()
                self.assertEqual(both, summarize(paths["P1"], paths["P2"]))
                snapshot.write_text(json.dumps(both))
                paths["P2"].rename(pending)
                with self.assertRaisesRegex(ValueError, "P2"):
                    report_review()
                paths["P1"].rename(folder / "archived-P1.xlsx")
                self.assertEqual(report_review(), both)
                with self.assertRaisesRegex(ValueError, "Không tìm thấy"):
                    report_review(folder)

    @unittest.skipUnless(find_spec("docx"), "Requires report/requirements.txt")
    def test_appendix_prints_current_counts_and_comparison(self):
        from docx import Document
        from report.pilot5_acceptance import append_acceptance

        with tempfile.TemporaryDirectory() as temp:
            paths = example_ballots(Path(temp))
            for p2, expected, complete in [(HERE / "P2.xlsx", "1/2 phiếu hoàn tất và 6/12", False),
                                           (paths["P2"], "2/2 phiếu hoàn tất và 12/12", True)]:
                doc = Document(HERE.parent / "report/mau_bien_tap.docx")
                append_acceptance(doc, summarize(paths["P1"], p2))
                text = "\n".join(p.text for p in doc.paragraphs)
                self.assertIn(expected, text)
                self.assertEqual("K  Kết quả hai phiếu chấm độc lập" in text, complete)
                if complete:
                    self.assertIn("5/6 hồ sơ", text)
                    self.assertIn("R2", text)
                    self.assertEqual([c.text for c in doc.tables[-1].rows[2].cells[1:]], ["1/3", "0/3"])
