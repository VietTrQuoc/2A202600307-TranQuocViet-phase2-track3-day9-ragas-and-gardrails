from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_THRESHOLDS = {
    "faithfulness": 0.85,
    "answer_relevancy": 0.80,
    "context_precision": 0.70,
    "context_recall": 0.75,
}


def parse_thresholds(values: list[str]) -> dict[str, float]:
    thresholds = DEFAULT_THRESHOLDS.copy()
    for item in values:
        key, raw = item.split("=", 1)
        thresholds[key] = float(raw)
    return thresholds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", default="phase-a/ragas_summary.json")
    parser.add_argument("--threshold", nargs="*", default=[])
    args = parser.parse_args()

    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    thresholds = parse_thresholds(args.threshold)
    failures = []
    for metric, target in thresholds.items():
        actual = float(summary[metric])
        if actual < target:
            failures.append(f"{metric}: {actual:.3f} < {target:.3f}")
    if failures:
        print("Eval gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Eval gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
