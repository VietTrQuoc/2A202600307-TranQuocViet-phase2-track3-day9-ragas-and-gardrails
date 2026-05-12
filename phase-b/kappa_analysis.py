from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cohen_kappa(a: list[str], b: list[str]) -> float:
    labels = sorted(set(a) | set(b))
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    expected = 0.0
    for label in labels:
        pa = sum(x == label for x in a) / n
        pb = sum(x == label for x in b) / n
        expected += pa * pb
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def interpret(kappa: float) -> str:
    if kappa < 0:
        return "Worse than chance"
    if kappa < 0.2:
        return "Slight agreement"
    if kappa < 0.4:
        return "Fair agreement"
    if kappa < 0.6:
        return "Moderate agreement"
    if kappa < 0.8:
        return "Substantial agreement"
    return "Almost perfect agreement"


if __name__ == "__main__":
    human = read_csv(ROOT / "phase-b" / "human_labels.csv")
    judge = read_csv(ROOT / "phase-b" / "pairwise_results.csv")[:10]
    h = [row["human_winner"] for row in human]
    j = [row["winner_after_swap"] for row in judge]
    score = cohen_kappa(h, j)
    print(f"Cohen's kappa: {score:.3f}")
    print(interpret(score))
