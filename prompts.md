# Prompts Used

## Synthetic Test Set
Generate banking-support RAG evaluation questions from policy-style chunks with a 50 percent simple, 25 percent reasoning, and 25 percent multi-context distribution. Each question must include a grounded answer and source context.

## Pairwise Judge
You are an impartial evaluator. Compare two answers to the same question based on factual accuracy, relevance, conciseness, and helpfulness. Output JSON only with `winner` and `reason`.

## Swap-And-Average Bias Mitigation
Evaluate the same pair twice with answer order swapped. Flip the second winner back to the original answer identity. If both runs agree, keep the winner; otherwise return `tie`.

## Absolute Rubric
Score the answer from 1 to 5 on factual accuracy, relevance, conciseness, and helpfulness. Compute overall as the arithmetic mean of the four dimensions.

## Topic Guard
Allow banking, loan, card, fraud, interest, repayment, account, customer, policy, and OTP questions. Refuse unrelated topics with a helpful message that redirects users to supported banking-support topics.
