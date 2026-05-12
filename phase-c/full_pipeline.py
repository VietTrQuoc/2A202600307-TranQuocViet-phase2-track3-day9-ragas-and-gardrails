from __future__ import annotations

import asyncio
import csv
import time
from pathlib import Path

from input_guard import InputGuard, TopicGuard
from output_guard import OutputGuard


ROOT = Path(__file__).resolve().parents[1]
input_guard = InputGuard()
topic_guard = TopicGuard()
output_guard = OutputGuard()


def refuse_response(reason: str = "Request refused by guardrail.") -> str:
    return f"I cannot answer that request. {reason}"


async def rag_pipeline_async(question: str) -> str:
    await asyncio.sleep(0.01)
    return (
        "Based on the banking support policy, verify the customer, use the approved "
        "workflow, and cite only retrieved policy facts."
    )


async def audit_log(user_input: str, answer: str, timings: dict[str, float]) -> None:
    line = {"input": user_input[:80], "answer": answer[:80], **timings}
    path = ROOT / "phase-c" / "audit_log.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(str(line) + "\n")


async def guarded_pipeline(user_input: str) -> tuple[str, dict[str, float]]:
    timings: dict[str, float] = {}

    t0 = time.perf_counter()
    pii_task = asyncio.create_task(input_guard.sanitize_async(user_input))
    topic_task = asyncio.create_task(topic_guard.check_async(user_input))
    sanitized, _, _ = await pii_task
    topic_ok, topic_reason = await topic_task
    injection, injection_reason = input_guard.detect_injection(user_input)
    timings["L1"] = (time.perf_counter() - t0) * 1000

    if not topic_ok:
        return refuse_response(topic_reason), timings
    if injection:
        return refuse_response(injection_reason), timings

    t0 = time.perf_counter()
    answer = await rag_pipeline_async(sanitized)
    timings["L2"] = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    safe, reason, _ = await output_guard.check_async(sanitized, answer)
    timings["L3"] = (time.perf_counter() - t0) * 1000
    if not safe:
        return refuse_response(reason), timings

    asyncio.create_task(audit_log(user_input, answer, timings))
    return answer, timings


async def benchmark(n: int = 100) -> list[dict[str, float]]:
    queries = [
        "How do I activate a new card after OTP verification?",
        "What affects loan eligibility for a customer?",
        "How should fraud reporting work for a suspicious card transaction?",
        "Can a customer repay a loan early?",
    ]
    rows = []
    for i in range(n):
        _, timings = await guarded_pipeline(queries[i % len(queries)])
        rows.append({"request_id": i + 1, **timings})
    return rows


if __name__ == "__main__":
    data = asyncio.run(benchmark())
    path = ROOT / "phase-c" / "latency_benchmark_live.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["request_id", "L1", "L2", "L3"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {path}")
