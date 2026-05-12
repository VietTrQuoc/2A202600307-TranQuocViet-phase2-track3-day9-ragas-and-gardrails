# Failure Cluster Analysis

## Bottom 10 Questions

| # | Question | Type | F | AR | CP | CR | Avg | Cluster |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | How should support combine card safety and customer notification steps | multi_context | 0.51 | 0.6 | 0.43 | 0.522 | 0.515 | C1 |
| 2 | How should support combine card safety and customer notification steps | multi_context | 0.51 | 0.612 | 0.47 | 0.51 | 0.525 | C1 |
| 3 | How should support combine card safety and customer notification steps | multi_context | 0.57 | 0.6 | 0.45 | 0.498 | 0.529 | C1 |
| 4 | How should support combine card safety and customer notification steps | multi_context | 0.555 | 0.624 | 0.45 | 0.498 | 0.532 | C1 |
| 5 | How should support combine card safety and customer notification steps | multi_context | 0.525 | 0.6 | 0.47 | 0.546 | 0.535 | C1 |
| 6 | How should support combine card safety and customer notification steps | multi_context | 0.57 | 0.624 | 0.43 | 0.522 | 0.536 | C1 |
| 7 | How should support combine card safety and customer notification steps | multi_context | 0.54 | 0.624 | 0.47 | 0.546 | 0.545 | C1 |
| 8 | Given income and debt checks, why might application 6 be rejected? | reasoning | 0.585 | 0.684 | 0.51 | 0.558 | 0.584 | C2 |
| 9 | Given income and debt checks, why might application 8 be rejected? | reasoning | 0.615 | 0.66 | 0.49 | 0.582 | 0.587 | C2 |
| 10 | Given income and debt checks, why might application 4 be rejected? | reasoning | 0.63 | 0.66 | 0.53 | 0.606 | 0.607 | C2 |

## Clusters Identified

### Cluster C1: Cross-document retrieval misses
Pattern: multi-context questions need both security and customer-operations chunks, but top-k retrieval often returns only one side.
Examples: incident 2 and incident 4 support-flow questions.
Proposed fix: increase top_k from 3 to 6, add hybrid BM25 + vector retrieval, then rerank with a cross-encoder.

### Cluster C2: Reasoning compression failures
Pattern: rejection/eligibility questions require combining income, debt ratio, and document status.
Examples: applications 5 and 7 rejection questions.
Proposed fix: add query decomposition for policy conditions and retrieve one chunk per condition before generation.
