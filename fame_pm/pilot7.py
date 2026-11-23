"""Check the original Pilot 7 threshold validator against its public sensor configuration."""
import argparse
import csv
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REVISION = "d5eb4c69addf9078c5d80042ea2229f50a43ed41"


def run(checkout):
    checkout = checkout.resolve()
    revision = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
    if revision != REVISION:
        raise ValueError(f"Expected upstream commit {REVISION}, got {revision}")
    subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--",
                    "backend/config/tags.csv", "worker/src"], check=True)
    sys.path.insert(0, str(checkout))
    from worker.src.quality_assessment import QualityAssessmentEngine

    engine = QualityAssessmentEngine()
    with (checkout / "backend/config/tags.csv").open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if len({row["TAG"] for row in rows}) != len(rows):
        raise ValueError("Sensor tags must be unique")
    skipped = []
    invalid_configuration = {}
    checks = 0
    for row in rows:
        tag, kind = row["TAG"], row["THRESHOLD_TYPE"]
        if not kind:
            skipped.append(tag)
            continue
        try:
            low = float(row["LOW_THRESHOLD"]) if row["LOW_THRESHOLD"] else None
            high = float(row["HIGH_THRESHOLD"]) if row["HIGH_THRESHOLD"] else None
        except ValueError:
            invalid_configuration[tag] = {key: row[key] for key in ("LOW_THRESHOLD", "HIGH_THRESHOLD")}
            continue
        if kind not in {"Up", "Down", "Up/Down"}:
            raise ValueError(f"Unknown threshold type for {tag}")
        bounds = []
        if kind in {"Down", "Up/Down"}:
            bounds.append((low, (False, True, True)))
        if kind in {"Up", "Up/Down"}:
            bounds.append((high, (True, True, False)))
        # Load the published thresholds in memory, as the worker does after a database read.
        engine.thresholds_cache[tag] = {"threshold_type": kind, "low_threshold": low, "high_threshold": high}
        for threshold, expectations in bounds:
            if threshold is None or not math.isfinite(threshold):
                raise ValueError(f"Missing or invalid configured bound for {tag}")
            cases = (math.nextafter(threshold, -math.inf), threshold, math.nextafter(threshold, math.inf))
            for value, expected in zip(cases, expectations):
                actual = engine.validate_value(tag, value)
                if actual != (expected, "valid" if expected else "invalid"):
                    raise ValueError(f"{tag}: unexpected classification at {value!r}: {actual!r}")
                checks += 1
    return dict(upstream="https://github.com/giorgosfatouros/IIoT-Data-Quality-Assessment",
                commit=revision, configuration="backend/config/tags.csv",
                function="worker.src.quality_assessment.QualityAssessmentEngine.validate_value",
                configured_rows=len(rows), tested_tags=len(rows) - len(skipped) - len(invalid_configuration),
                non_numeric_thresholds=invalid_configuration,
                tags_without_threshold_type=skipped, boundaries=checks // 3, passed_boundary_cases=checks,
                observations="Constructed boundary values; historical plant telemetry was not used.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run(args.checkout)
    if args.check:
        expected = json.loads((ROOT / "results/pilot7_boundaries.json").read_text())
        if result != expected:
            raise SystemExit("Pilot 7 result differs from the published file")
        print(f"Verified {result['passed_boundary_cases']} boundary cases on {result['tested_tags']} tags")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
