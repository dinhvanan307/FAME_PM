"""Check the released audit against the original signal keys and dated FAME image."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


class MarketSenseRelease(unittest.TestCase):
    def test_dated_evidence_stays_with_its_original_key(self):
        signal_file = "esg-data-audit/marketsense-sp100/MarketSenseAI_data_SP100.csv"
        self.assertEqual(hashlib.md5((ROOT / signal_file).read_bytes()).hexdigest(),
                         "f0bec18331b82b25282cc4a572a71d47")
        signals = {r[""]: r for r in read_csv(signal_file)}
        source = {(r["ticker"], r["predicted_at"]): r for r in read_csv("evidence/pilot5_d64_p64.csv")}
        results = read_csv("results/marketsense_sp100.csv")
        summary = json.loads((ROOT / "results/marketsense_sp100.json").read_text())
        self.assertEqual(len(source), 22)
        self.assertEqual(len(results), len(signals))
        self.assertEqual({r["source_id"] for r in results}, signals.keys())
        self.assertEqual(Counter(r["decision"] for r in signals.values()), summary["by_decision"])
        matched = 0
        for row in results:
            original = signals[row["source_id"]]
            self.assertEqual((row["ticker"], row["date"], row["decision"]),
                             (original["ticker"], original["date"], original["decision"]))
            image_row = source.get((original["ticker"], original["date"]))
            self.assertEqual(row["d64_key_matched"], str(int(image_row is not None)))
            for column in ("display_id", "env", "soc", "gov", "signal"):
                self.assertEqual(row["d64_" + column], image_row[column] if image_row else "")
            matched += image_row is not None
        self.assertEqual(matched, len(source))
        self.assertEqual(summary["d64_pdf_page_64"]["matched_ticker_date"], matched)
        self.assertEqual(summary["zenodo_esg"]["verifiable_ticker_date_pairs"], 0)
