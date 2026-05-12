# Judge Bias Report

## Bias 1: Position Bias
The pairwise judge ran every comparison twice with answer order swapped. In the offline run, Answer A wins most non-tie cases because it is intentionally the more grounded answer, but swap-and-average prevents a first-position win from being accepted unless the swapped run agrees after winner normalization.

Observed signal:
- Run 1 `A` wins: 24/30.
- Final ties after swap disagreement: 9/30.
- Mitigation: swap answer order, normalize the second result, and convert disagreements to `tie`.

## Bias 2: Length Bias
Answer B sometimes contains extra unrelated detail. A naive judge may reward longer answers even when grounding is weaker. The absolute rubric separates factual accuracy, relevance, conciseness, and helpfulness so verbosity cannot dominate the total score.

Observed signal:
- Long but less specific answers were downgraded on conciseness.
- Grounded concise answers still won when they directly cited policy conditions.
- Mitigation: cap answer length in production eval samples and keep conciseness as a separate rubric dimension.

## Calibration Note
Human labels in `human_labels.csv` prioritize groundedness over style. The current kappa score is acceptable for monitoring, but production use should label at least 30 to 50 pairs per major prompt or retriever change.
