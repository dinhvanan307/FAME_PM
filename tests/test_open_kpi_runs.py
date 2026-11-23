import unittest

from fame_pm.open_kpi_runs import weighting_trials


class WeightTrials(unittest.TestCase):
    def test_each_pure_pillar_picks_its_own_winner(self):
        tickers = ["A", "B", "C", "D", "E", "F"]
        data = {}
        for i, axis in enumerate("esg"):
            row = ["0"] * len(tickers)
            row[i] = "1"
            data["_esg_" + axis] = (tickers, [row, row])
        result = weighting_trials(data)
        self.assertEqual(result["unique_input_panels"], 1)
        self.assertEqual(result["ordinal_rows"], 2)
        self.assertEqual(len(result["profiles"]), 15)
        for profile in result["profiles"]:
            self.assertEqual(sum(profile["weights_percent"]), 100)
            if profile["weight_percent"] == 100:
                expected = dict(E="A", S="B", G="C")[profile["pillar"]]
                self.assertEqual(profile["last_row_top5"][0], expected)

    def test_mismatched_tickers_are_rejected(self):
        data = {
            "_esg_e": (["A"], [["60"]]),
            "_esg_s": (["B"], [["60"]]),
            "_esg_g": (["A"], [["60"]]),
        }
        with self.assertRaisesRegex(ValueError, "Unaligned"):
            weighting_trials(data)
