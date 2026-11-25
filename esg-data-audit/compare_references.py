"""Compare two reference rules against the original FAME ESG exports by row position."""
import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import fmean

from reproduce_pilot5 import DOI, PILLARS, TOL, load_exports

HERE = Path(__file__).resolve().parent


def compare(directory):
    _, manifest, tables = load_exports(directory)
    pinned = json.loads((HERE / "reproduction.json").read_text())["csv_manifest"]
    if manifest != pinned:
        raise ValueError("Original CSV checksums or dimensions differ from the published baseline")
    totals = tables["total"]
    sectors = tables["sector_daily"]
    adjusted_totals = tables["adj"]
    first_mean = fmean(sectors[0].values())
    named = {}
    mean_group = []
    for ticker in sorted(totals[0]):
        implied = totals[0][ticker] - adjusted_totals[0][ticker]
        candidates = [s for s, v in sectors[0].items() if abs(implied - v) <= TOL]
        if len(candidates) == 1:
            named[ticker] = candidates[0]
        elif not candidates and abs(implied - first_mean) <= TOL:
            mean_group.append(ticker)

    # References below use only the raw scores and sector export on each evaluation row.
    # The adjusted exports are read as outcomes after the estimates are computed.
    named_matches = mean_matches = frozen_matches = adjusted_total_matches = 0
    max_error = 0
    reference_counts = Counter()
    for i in range(1, len(totals)):
        mean = fmean(sectors[i].values())
        reference_counts[mean] += 1
        for ticker in (*named, *mean_group):
            is_named = ticker in named
            reference = sectors[i][named[ticker]] if is_named else mean
            adjustment = totals[i][ticker] - reference
            if not is_named:
                adjusted_total_matches += abs(adjustment - adjusted_totals[i][ticker]) <= TOL
            for pillar in PILLARS:
                raw = tables[pillar][i][ticker]
                actual = tables[pillar + "_adj"][i][ticker]
                error = abs(raw + adjustment - actual)
                max_error = max(max_error, error)
                if is_named:
                    named_matches += error <= TOL
                else:
                    mean_matches += error <= TOL
                    frozen_estimate = raw + totals[i][ticker] - first_mean
                    frozen_matches += abs(frozen_estimate - actual) <= TOL

    n = len(totals) - 1
    cells = n * len(PILLARS)
    return {
        "source_doi": DOI,
        "absolute_tolerance": TOL,
        "calibration_row": 1,
        "evaluation_rows": [2, len(totals)],
        "sector_columns": list(sectors[0]),
        "denominator_pillar_cells": cells * len(totals[0]),
        "named_sector_only": {"covered_tickers": len(named), "tested": cells * len(named), "matched": named_matches},
        "named_or_mean": {"covered_tickers": len(named) + len(mean_group), "tested": cells * (len(named) + len(mean_group)),
                          "matched": named_matches + mean_matches, "max_absolute_error": max_error},
        "additional_tickers": mean_group,
        "unresolved": sorted(totals[0].keys() - named.keys() - set(mean_group)),
        "additional_pillar_cells": {"tested": cells * len(mean_group), "matched": mean_matches,
                                    "matched_with_frozen_first_reference": frozen_matches},
        "additional_total_adjustment_cells": {"tested": n * len(mean_group), "matched": adjusted_total_matches},
        "evaluation_reference_values": [{"value": v, "rows": count} for v, count in sorted(reference_counts.items())],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--check", action="store_true", help="Compare with the committed observations")
    args = parser.parse_args()
    result = compare(args.data_dir)
    if args.check:
        if result != json.loads((HERE / "reference_comparison.json").read_text()):
            raise SystemExit("Reference comparison differs from the saved result")
        print(f"Matched {result['named_or_mean']['matched']} of {result['denominator_pillar_cells']} pillar cells.")
    else:
        print(json.dumps(result, indent=2, allow_nan=False))
