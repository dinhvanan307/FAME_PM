"""Use temporary, synthetic ballots to exercise the release and reconciliation rules."""
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from openpyxl import load_workbook

from Pilot5_nghiem_thu.tong_hop import HERE, SPEC, summarize


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
            paths = {}
            for person in ("P1", "P2"):
                book = load_workbook(HERE / f"{person}.xlsx")
                paths[person] = Path(temp) / f"{person}.xlsx"
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
