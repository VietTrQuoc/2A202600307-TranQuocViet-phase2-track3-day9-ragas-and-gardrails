from __future__ import annotations

import asyncio
import re
import time


VN_PII = {
    "cccd": r"\b\d{12}\b",
    "phone_vn": r"\b(?:\+84|0)\d{9,10}\b",
    "tax_code": r"\b\d{10}(?:-\d{3})?\b",
    "email": r"\b[\w.-]+@[\w.-]+\.\w+\b",
}

INJECTION_PATTERNS = [
    r"ignore (all )?(previous|system|developer) instructions",
    r"\bDAN\b",
    r"jailbreak",
    r"without restrictions",
    r"bypass",
    r"decode this base64",
]


class InputGuard:
    """PII redaction and lightweight prompt-injection detection."""

    def scrub_vn(self, text: str) -> tuple[str, bool]:
        found = False
        out = text or ""
        for name, pattern in VN_PII.items():
            out, n = re.subn(pattern, f"[{name.upper()}]", out, flags=re.IGNORECASE)
            found = found or n > 0
        return out, found

    def scrub_ner_fallback(self, text: str) -> tuple[str, bool]:
        found = False
        patterns = {
            "PERSON": r"\b(?:John Smith|Nguyen Van A|Ly Van Binh)\b",
            "ORG": r"\b(?:Microsoft|OpenAI|VinUniversity)\b",
            "ADDRESS": r"\b\d{1,5}\s+[A-Z][A-Za-z ]+\b",
            "PHONE": r"\+1-\d{3}-\d{4}",
        }
        out = text
        for name, pattern in patterns.items():
            out, n = re.subn(pattern, f"[{name}]", out)
            found = found or n > 0
        return out, found

    def detect_injection(self, text: str) -> tuple[bool, str]:
        lowered = text.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, lowered, flags=re.IGNORECASE):
                return True, f"Injection pattern matched: {pattern}"
        return False, "No injection pattern matched"

    def sanitize(self, text: str) -> tuple[str, float, bool]:
        start = time.perf_counter()
        cleaned, vn_found = self.scrub_vn(text)
        cleaned, ner_found = self.scrub_ner_fallback(cleaned)
        latency_ms = (time.perf_counter() - start) * 1000
        return cleaned, latency_ms, vn_found or ner_found

    async def sanitize_async(self, text: str) -> tuple[str, float, bool]:
        return await asyncio.to_thread(self.sanitize, text)


class TopicGuard:
    def __init__(self, allowed_topics: list[str] | None = None) -> None:
        self.allowed_topics = allowed_topics or ["banking", "loans", "cards", "fraud", "interest", "repayment"]
        self.keywords = {
            "banking",
            "loan",
            "loans",
            "card",
            "cards",
            "fraud",
            "interest",
            "repayment",
            "account",
            "customer",
            "policy",
            "otp",
        }

    def check(self, text: str) -> tuple[bool, str]:
        tokens = set(re.findall(r"[a-zA-Z]+", (text or "").lower()))
        if tokens & self.keywords:
            return True, "On topic: banking support"
        return False, "I can help with banking, loan, card, and fraud-support questions only."

    async def check_async(self, text: str) -> tuple[bool, str]:
        return await asyncio.to_thread(self.check, text)
