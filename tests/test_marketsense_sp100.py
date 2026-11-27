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
    def test_date_index_inventory_agrees_with_the_verified_csv_release(self):
        audit = json.loads((ROOT / "results/pilot5_zenodo_inventory.json").read_text())
        reference = json.loads((ROOT / "esg-data-audit/reproduction.json").read_text())["csv_manifest"]
        files = {item["file"]: item for item in audit["files"] if item["file"].endswith(".csv")}
        self.assertEqual(files.keys(), reference.keys())
        for name, item in files.items():
            self.assertEqual((item["checksum"], item["rows"], item["columns"]),
                             (reference[name]["md5"], reference[name]["rows"], reference[name]["columns"]))
            self.assertEqual(item["ticker_columns"] + len(item["other_columns"]), item["columns"])
        sector_table, = [item for item in files.values() if item["other_columns"]]
        self.assertTrue(sector_table["file"].endswith("_esg_sector_daily.csv"))
        self.assertEqual(sector_table["ticker_columns"], 0)
        self.assertEqual(set(sector_table["other_columns"]), {
            "Basic Materials", "Consumer Goods", "Energy", "Financial Services",
            "Healthcare", "Real Estate", "Technology", "Utilities"})

    def test_public_source_review_preserves_exact_keys_and_exclusions(self):
        summary = json.loads((ROOT / "results/marketsense_sp100.json").read_text())
        review = summary["source_review"]
        verified = read_csv("results/marketsense_esg_matches.csv")
        by_key = {(r["ticker"], r["date"]): r for r in verified}
        d64 = read_csv("evidence/pilot5_d64_p64.csv")
        self.assertEqual(len(by_key), len(verified))
        self.assertEqual(set(by_key), {(r["ticker"], r["predicted_at"]) for r in d64})
        for row in d64:
            match = by_key[row["ticker"], row["predicted_at"]]
            self.assertEqual([match[p] for p in ("env", "soc", "gov")],
                             [row[p] for p in ("env", "soc", "gov")])
            self.assertTrue(match["url"].endswith("#page=64"))
            self.assertEqual(match["date_role"], "predicted_at")
            self.assertEqual(match["locator"], "PDF 64, display ID " + row["display_id"])
        self.assertEqual((review["baseline"], review["added"], review["verified"], review["open"]),
                         (len(d64), 0, len(verified), summary["observations"] - len(verified)))
        reasons = {(r["ticker"], r["period"]): r["decision_reasons"] for r in review["candidate_review"]}
        for year in ("2016", "2017", "2018"):
            self.assertIn("year_only", reasons["NVDA.US", year])
            self.assertIn("illustrative_example", reasons["NVDA.US", year])
        self.assertIn("no_separate_pillars", reasons["ABBV.US", "2025-09-19"])
        self.assertIn("no_exact_signal_key", reasons["ABBV.US", "2025-09-19"])

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
