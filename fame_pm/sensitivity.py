"""Measure how two ESG weighting profiles affect the shortlist on every ordinal row."""

import csv
from decimal import Decimal

from .analysis import require


def order_scores(scores):
    """Break exact score ties by ticker, as in the original one-row reproduction."""
    return sorted(scores, key=lambda ticker: (-scores[ticker], ticker))


def shortlist_change(equal, green, size=5):
    base, alternative = order_scores(equal), order_scores(green)
    a, b = base[:size], alternative[:size]
    base_tie = len(base) > size and equal[base[size - 1]] == equal[base[size]]
    alt_tie = len(alternative) > size and green[alternative[size - 1]] == green[alternative[size]]
    common = len(set(a) & set(b))
    return common, a == b, base_tie or alt_tie, a, b


def panel_sensitivity(directory, reproduction):
    # Called after the original files have passed their Zenodo checksum checks.
    data = []
    for pillar in ("e", "s", "g"):
        (name,) = [k for k in reproduction["csv_manifest"] if k.endswith(f"_esg_{pillar}.csv")]
        with (directory / name).open(encoding="utf-8-sig", newline="") as f:
            table = []
            for row in csv.DictReader(f):
                values = {k: Decimal(v) * 100 for k, v in row.items()}
                require(
                    all(v.is_finite() and v == v.to_integral_value() for v in values.values()),
                    f"Expected original pillar scores at cent precision in {name}",
                )
                table.append({k: int(v) for k, v in values.items()})
            data.append(table)
    require(len({len(t) for t in data}) == 1 and data[0], "Pillar rows do not align")
    tickers = set(data[0][0])
    overlaps = [0] * 6
    rank_pairs = set()
    identical_order = cutoff_ties = unchanged_without_tie = 0
    for e, s, g in zip(*data):
        require(tickers == set(e) == set(s) == set(g), "Pillar tickers do not align")
        equal = {k: e[k] + s[k] + g[k] for k in tickers}
        green = {k: 3 * e[k] + s[k] + g[k] for k in tickers}
        common, same_order, tie, last_equal, last_green = shortlist_change(equal, green)
        rank_pairs.add((tuple(last_equal), tuple(last_green)))
        overlaps[common] += 1
        identical_order += same_order
        cutoff_ties += tie
        unchanged_without_tie += common == 5 and not tie
    snapshot = reproduction["ranking_sensitivity"]
    require(
        last_equal == snapshot["top5_equal"] and last_green == snapshot["top5_environment"],
        "Final ordinal row does not reproduce the original scenario",
    )
    n = len(data[0])
    return dict(
        rows=n,
        tickers=len(tickers),
        top_k=5,
        scores="original E/S/G",
        weights=[[1, 1, 1], [3, 1, 1]],
        tie_rule="ticker ascending",
        overlap_histogram={str(i): v for i, v in enumerate(overlaps)},
        identical_members=overlaps[5],
        different_members=n - overlaps[5],
        identical_order=identical_order,
        distinct_top5_pairs=len(rank_pairs),
        reordered_same_members=overlaps[5] - identical_order,
        cutoff_tie_rows=cutoff_ties,
        no_cutoff_tie_rows=n - cutoff_ties,
        identical_members_without_cutoff_tie=unchanged_without_tie,
        mean_shared=sum(i * v for i, v in enumerate(overlaps)) / n,
        last_row_equal=last_equal,
        last_row_environment=last_green,
    )
