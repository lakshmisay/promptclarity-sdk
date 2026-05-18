"""Unsafe, sensitive, and vague input checks."""

from __future__ import annotations

import re
from typing import List

from promptclarity.types import RiskReport


SENSITIVE_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "phone": re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "api_key": re.compile(r"\b(?:sk-|api[_-]?key|secret|token)\w*", re.IGNORECASE),
}

UNSAFE_TERMS = {
    "bypass",
    "exploit",
    "steal",
    "malware",
    "phishing",
    "credential",
}

VAGUE_RISK_TERMS = {
    "anything",
    "whatever",
    "asap",
    "just do it",
}


def assess_risk(prompt: str) -> RiskReport:
    normalized = prompt.lower()
    signals: List[str] = []

    for label, pattern in SENSITIVE_PATTERNS.items():
        if pattern.search(prompt):
            signals.append(f"sensitive_{label}")

    for term in UNSAFE_TERMS:
        if term in normalized:
            signals.append(f"unsafe_term_{term}")

    for term in VAGUE_RISK_TERMS:
        if term in normalized:
            signals.append(f"vague_instruction_{term.replace(' ', '_')}")

    if any(signal.startswith("unsafe") for signal in signals):
        level = "high"
    elif any(signal.startswith("sensitive") for signal in signals):
        level = "medium"
    elif signals:
        level = "low"
    else:
        level = "low"

    return RiskReport(level=level, signals=signals)
