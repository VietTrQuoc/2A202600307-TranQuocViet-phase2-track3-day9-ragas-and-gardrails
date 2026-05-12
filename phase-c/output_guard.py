from __future__ import annotations

import asyncio
import re
import time


UNSAFE_PATTERNS = [
    r"how to hack",
    r"steal",
    r"phishing",
    r"malware",
    r"bypass authentication",
    r"commit fraud",
    r"exfiltrate",
    r"disable safety",
]


class OutputGuard:
    """Local Llama-Guard-style fallback for environments without GPU/API keys."""

    model_name = "llama-guard-3-8b-compatible-local-fallback"

    def check(self, user_input: str, agent_response: str) -> tuple[bool, str, float]:
        start = time.perf_counter()
        text = f"{user_input}\n{agent_response}".lower()
        unsafe_hits = [p for p in UNSAFE_PATTERNS if re.search(p, text)]
        latency_ms = (time.perf_counter() - start) * 1000
        if unsafe_hits:
            return False, f"unsafe: matched {unsafe_hits[0]}", latency_ms
        return True, "safe", latency_ms

    async def check_async(self, user_input: str, agent_response: str) -> tuple[bool, str, float]:
        return await asyncio.to_thread(self.check, user_input, agent_response)
