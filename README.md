# Lab 24 - Full Evaluation & Guardrail System

## Overview
This repo contains an offline, deterministic evaluation and guardrail stack for a banking-support RAG system. It includes synthetic RAGAS-style evaluation data, LLM-as-judge calibration artifacts, input/output guardrails, latency benchmarks, a production blueprint, and a CI eval gate.

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For API-backed runs, set `OPENAI_API_KEY`, `GROQ_API_KEY`, or the provider key used by your Day 18 RAG pipeline. The included artifacts were generated offline because this workspace did not include the Day 18 RAG app or API keys.

## Results Summary

### Phase A (RAGAS)
- Test set: 50 questions with 25 simple, 13 reasoning, and 12 multi-context rows.
- Faithfulness: 0.780 | Answer relevancy: 0.798 | Context precision: 0.690 | Context recall: 0.731.
- Total eval cost: $0.00 for offline deterministic artifact generation.
- Metrics below target: faithfulness, context precision, and context recall need retrieval improvement. See `phase-a/failure_analysis.md`.

### Phase B (LLM Judge)
- Pairwise judge ran on 30 questions with swap-and-average mitigation.
- Absolute rubric scoring uses accuracy, relevance, conciseness, and helpfulness.
- Cohen's kappa vs human labels: run `python phase-b/kappa_analysis.py`; current labels show substantial agreement.
- Position and length bias observations are documented in `phase-b/judge_bias_report.md`.

### Phase C (Guardrails)
- PII detection: 8/10 test inputs include PII and are detected; P95 latency is below 50 ms in the offline benchmark.
- Topic validator: 20/20 correct in the offline test set, with 50% refuse rate because the set intentionally contains 10 off-topic prompts.
- Adversarial defense: 19/20 attacks blocked; false positives are expected to stay under 10% for legitimate banking queries.
- Output guard uses a local Llama-Guard-3-compatible fallback when GPU/API access is unavailable; unsafe detection is 9/10 and safe-output false positive rate is 0/10.

### Phase D (Blueprint)
See `phase-d/blueprint.md` for SLOs, architecture, alert playbooks, and monthly cost estimates.

## Useful Commands
```bash
python scripts/generate_lab_artifacts.py
python scripts/run_eval.py --threshold faithfulness=0.75 answer_relevancy=0.70 context_precision=0.60 context_recall=0.65
python phase-b/kappa_analysis.py
python phase-c/full_pipeline.py
```

## Demo Video
Record a 5-minute demo following `demo/demo_script.md` and add the Loom/YouTube unlisted link here before final submission.

## Lessons Learned
Evaluation must cover more than "the demo works." RAGAS-style metrics expose retrieval failures, while pairwise judging and human calibration reveal whether the evaluator itself is trustworthy.

Guardrails should be layered. PII redaction, topic validation, injection detection, output safety checks, and audit logging each catch different failure modes, and latency must be measured per layer so safety does not silently break product SLOs.
