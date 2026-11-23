import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fame_pm.analysis import pm_results
from fame_pm.reviews import COLUMNS, BLOCKS, verify_reviews
from fame_pm.sensitivity import shortlist_change


class ReproductionTests(unittest.TestCase):
    def test_cutoff_tie_and_order(self):
        scores = {"C": 3, "B": 2, "A": 2}
        common, same, tie, a, b = shortlist_change(scores, {"A": 1, "B": 2, "C": 3}, size=2)
        self.assertEqual((common, same, tie, a, b), (1, False, True, ["C", "A"], ["C", "B"]))

    def test_same_members_can_be_reordered(self):
        common, same, tie, *_ = shortlist_change({"A": 1, "B": 2}, {"A": 2, "B": 1}, 2)
        self.assertEqual((common, same, tie), (2, False, False))

    def test_private_verification_uses_original_rows(self):
        # Synthetic timestamps and votes. Only the test fixture is written to disk.
        result = pm_results()
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for person, blocks in BLOCKS.items():
                clock = datetime(2001, 1, 1, tzinfo=timezone.utc)
                records = [COLUMNS]
                for turn, (mode, ids) in enumerate(blocks, 1):
                    for number in ids:
                        end = clock + timedelta(seconds=2)
                        times = [t.isoformat().replace("+00:00", "Z") for t in (clock, end)]
                        vote = "Duyệt" if number <= 3 else "Không duyệt"
                        method = "Thông thường" if mode == "A" else "Có gợi ý checklist"
                        records.append([person, turn, method, f"K{number:02}", vote, *times, "2"])
                        clock = end
                with (directory / f"FAME_{person}_duyet_nhanh.csv").open(
                    "w", newline="", encoding="utf-8"
                ) as f:
                    csv.writer(f).writerows(records)
            for mode in ("A", "B"):
                result["independent_review"][mode].update(
                    approvals=3, matches=6, false_approvals=0, total_seconds=12, median_seconds=2
                )
            verify_reviews(directory, result)
            file = directory / "FAME_P2_duyet_nhanh.csv"
            copy = directory / "FAME_P2_duyet_nhanh (1).csv"
            copy.write_bytes(file.read_bytes())
            verify_reviews(directory, result)
            copy.write_text("conflict", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Conflicting"):
                verify_reviews(directory, result)
            copy.unlink()
            file.write_text(file.read_text().replace("K04", "K03", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "assigned order"):
                verify_reviews(directory, result)
