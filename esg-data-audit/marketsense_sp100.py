"""Audit the published S&P 100 signals and join only evidence with dated ESG keys."""
import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import median

from reproduce_pilot5 import load_exports

ROOT = Path(__file__).resolve().parents[1]
SIGNALS = ROOT / "esg-data-audit/marketsense-sp100/MarketSenseAI_data_SP100.csv"
SNAPSHOT = ROOT / "evidence/pilot5_d64_p64.csv"
SIGNAL_SHA256 = "5b8b9bf3ac7a073939a67299d00dfbb766c9f396e8c7fae1b8d735dfbde2f6d0"
LABELS = ("buy", "hold", "sell")
# Each rule is an observable text marker, counted once per explanation.
MARKERS = {
    "news": r"\b(?:news|headline[s]?)\b",
    "price_risk": r"\b(?:price dynamics|momentum|volatility|sharpe|drawdown[s]?)\b",
    "macro": r"\b(?:macro(?:economic[s]?|economy)?|inflation|interest rates?|federal reserve)\b",
    "fundamentals": r"\b(?:fundamentals?|balance sheet[s]?|cash flow[s]?|earnings|revenues?)\b",
    "explicit_esg": r"\bESG\b|\benvironmental,?\s+social,?\s+(?:and\s+)?governance\b",
}
WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")


def dated_key(ticker, day):
    if not ticker or date.fromisoformat(day).isoformat() != day:
        raise ValueError(f"Invalid key: {ticker}, {day}")
    return ticker, day


def analyze(esg_dir):
    raw = SIGNALS.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SIGNAL_SHA256:
        raise ValueError("MarketSenseAI CSV differs from the pinned Zenodo release")
    signals = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
    if signals.fieldnames != ["", "ticker", "date", "decision", "why"]:
        raise ValueError("MarketSenseAI schema changed")
    with SNAPSHOT.open(encoding="utf-8", newline="") as source:
        snapshot = {}
        for row in csv.DictReader(source):
            key = dated_key(row["ticker"], row["predicted_at"])
            if key in snapshot or any(not row[p] for p in ("env", "soc", "gov")):
                raise ValueError(f"Duplicate or incomplete D6.4 observation: {key}")
            snapshot[key] = row

    _, manifest, tables = load_exports(esg_dir)
    pinned = json.loads((ROOT / "esg-data-audit/reproduction.json").read_text())["csv_manifest"]
    if manifest != pinned:
        raise ValueError("Pilot 5 CSV hashes, schema or row counts differ from the verified release")
    esg_tickers = set(tables["e"][0])
    if not all(symbol.endswith(".US") for symbol in esg_tickers):
        raise ValueError("Recheck ESG columns for non-ticker fields before assessing dates")

    monthly = defaultdict(Counter)
    flags = {name: re.compile(pattern, re.I) for name, pattern in MARKERS.items()}
    counts = {label: Counter() for label in LABELS}
    lengths = defaultdict(list)
    texts = set()
    keys, source_ids = set(), set()
    observed_symbols = set()
    output = []
    sample_matches = Counter()
    for row in signals:
        key = dated_key(row["ticker"], row["date"])
        if key in keys or row[""] in source_ids:
            raise ValueError(f"Duplicate signal key or CSV id: {key}")
        keys.add(key)
        source_ids.add(row[""])
        symbol, day = key
        observed_symbols.add(symbol)
        label = row["decision"]
        if label not in LABELS:
            raise ValueError(f"Unknown signal: {label}")
        monthly[day][label] += 1
        explanation = row["why"].strip()
        word_count = len(WORD.findall(explanation))
        if explanation:
            texts.add(" ".join(explanation.casefold().split()))
            lengths[label].append(word_count)
        markers = {name: int(bool(rule.search(explanation))) for name, rule in flags.items()}
        counts[label].update(markers)
        joined = snapshot.get(key)
        if joined:
            sample_matches["matched"] += 1
            sample_matches["same_label"] += int(joined["signal"].lower() == label)
        output.append({
            "source_id": row[""], "ticker": symbol, "date": day, "decision": label,
            "why_words": word_count, **markers, "ticker_in_zenodo_esg": int(symbol in esg_tickers),
            "d64_key_matched": int(joined is not None),
            **{f"d64_{col}": joined[col] if joined else "" for col in ("display_id", "signal", "env", "soc", "gov")},
        })
    totals = sum(monthly.values(), Counter())
    ordered_days = sorted(monthly)
    summary = {
        "signals_doi": "10.5281/zenodo.12744005", "signals_sha256": SIGNAL_SHA256,
        "pilot5_esg_doi": "10.5281/zenodo.17175084", "observations": len(keys),
        "unique_tickers": len(observed_symbols), "date_range": [ordered_days[0], ordered_days[-1]],
        "by_decision": {label: totals[label] for label in LABELS},
        "by_date": {day: {label: monthly[day][label] for label in LABELS} for day in ordered_days},
        "explanations_present": sum(map(len, lengths.values())), "distinct_normalized_texts": len(texts),
        "median_words_by_decision": {label: median(lengths[label]) if lengths[label] else None for label in LABELS},
        "marker_patterns": MARKERS, "marker_counts_by_decision": counts,
        "zenodo_esg": {
            "raw_pillar_rows": {p: len(tables[p]) for p in ("e", "s", "g")},
            "shared_tickers": len(esg_tickers & observed_symbols), "only_esg": sorted(esg_tickers - observed_symbols),
            "only_signals": sorted(observed_symbols - esg_tickers),
            "ticker_only_signal_rows": sum(row["ticker_in_zenodo_esg"] for row in output),
            "date_column": None, "verifiable_ticker_date_pairs": 0,
        },
        "d64_pdf_page_64": {
            "source_dates": sorted({day for _, day in snapshot}), "visible_rows": len(snapshot),
            "signal_counts_in_image": dict(Counter(r["signal"].lower() for r in snapshot.values())),
            "matched_ticker_date": sample_matches["matched"], "same_signal": sample_matches["same_label"],
            "unmatched_source_keys": [list(key) for key in sorted(snapshot.keys() - keys)],
            "signal_rows_without_snapshot": len(keys) - sample_matches["matched"],
        },
    }
    return summary, output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--esg-dir", type=Path, default=ROOT / "du_lieu/zenodo")
    parser.add_argument("--check", action="store_true", help="Compare both results to the published files")
    args = parser.parse_args()
    summary, rows = analyze(args.esg_dir)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=rows[0], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    artifacts = {"marketsense_sp100.json": json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                 "marketsense_sp100.csv": buffer.getvalue()}
    for name, content in artifacts.items():
        path = ROOT / "results" / name
        if args.check:
            if path.read_bytes() != content.encode():
                parser.exit(1, f"Published result differs: {name}\n")
        else:
            path.write_bytes(content.encode())
    print(f"{len(rows)} signals, {summary['d64_pdf_page_64']['matched_ticker_date']} dated image matches")


if __name__ == "__main__":
    main()
