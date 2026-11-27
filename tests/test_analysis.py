import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copyfile
import json

from fame_pm.analysis import ROOT, PASS, FAIL, OPEN, assess, pm_results, read_schedule


class EvidenceTests(unittest.TestCase):
    def test_measurement_boundaries(self):
        for direction, relation, v, expected in [
            ("<=", "<", 45, PASS),
            ("<=", "Giá trị", 60, PASS),
            ("<=", ">", 60, FAIL),
            ("<=", ">=", 60, OPEN),
            ("<=", "<", 61, OPEN),
            (">=", "<", 60, FAIL),
            (">=", "<=", 60, OPEN),
            (">=", ">=", 60, PASS),
            (">=", "Giá trị", 59, FAIL),
        ]:
            with self.subTest(direction=direction, relation=relation, v=v):
                self.assertEqual(assess(direction, 60, relation, v, "phút", "phút", True), expected)
        self.assertEqual(assess(">=", 0.7, None, None, "tỷ lệ", None, False), OPEN)
        self.assertEqual(assess(">=", 0.7, "Giá trị", 35, "tỷ lệ", "người", True), OPEN)
        self.assertEqual(assess(">=", 0.03, "Giá trị", 0.05, "tỷ lệ/năm", "tỷ lệ/năm", False), OPEN)

    def test_cover_and_calendar_must_agree(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evidence").mkdir()
            copyfile(ROOT / "FAME_Lich_MS_Project.xml", root / "FAME_Lich_MS_Project.xml")
            source = (
                (ROOT / "evidence/deliverables.csv").read_text().replace("2024-09-30", "2024-10-01")
            )
            (root / "evidence/deliverables.csv").write_text(source)
            with self.assertRaisesRegex(ValueError, "Cover"):
                read_schedule(root, json.loads((ROOT / "evidence/cordis.json").read_text()))

    def test_case_distinguishes_study_types(self):
        p = pm_results()
        schedule = p["schedule"]
        days = {r["deliverable"]: r["variance_days"] for r in schedule["deliverables"]}
        self.assertEqual(len(days), 32)
        self.assertEqual([days[k] for k in ("D1.2", "D2.1", "D4.2", "D6.4", "D6.3")],
                         [-1, 31, 53, 143, -8])
        self.assertEqual((days["D7.2"], days["D5.4"], days["D7.4"]), (333, 182, 0))
        self.assertEqual((schedule["late"], schedule["early"], schedule["on_deadline"],
                          schedule["median_signed_days"]), (22, 9, 1, 22))
        self.assertEqual(p["retrospective"]["A"]["matches"], 6)
        self.assertEqual(p["retrospective"]["B"]["with_owner"], 3)
        self.assertEqual(p["independent_review"]["B"]["matches"], 3)
        self.assertLess(p["independent_review"]["delta_mean_seconds"], 0)
        self.assertGreater(p["independent_review"]["delta_median_seconds"], 0)
        self.assertEqual(p["funding"][0]["other_eur"], "3731737.95")


if __name__ == "__main__":
    unittest.main()
