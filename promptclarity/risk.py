"""Unsafe, sensitive, and vague input checks."""

from __future__ import annotations

import re
from typing import List

from promptclarity.types import RiskReport


SENSITIVE_PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    "password": re.compile(r"\b(password|passwd|pwd)\s*[:=]\s*\S+", re.IGNORECASE),
    "phone": re.compile(r"\b(?:\+?\d[\d\s().-]{7,}\d)\b"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "api_key": re.compile(r"\b(?:sk-|api[_-]?key|secret|token)\w*", re.IGNORECASE),
}

UNSAFE_TERMS = {
    "bypass",
    "crack",
    "credential stuffing",
    "ddos",
    "exfiltrate",
    "exploit",
    "jailbreak",
    "keylogger",
    "steal",
    "malware",
    "phishing",
    "prompt injection",
    "ransomware",
    "sql injection",
    "credential",
}

VAGUE_RISK_TERMS = {
    "anything",
    "any way possible",
    "whatever",
    "asap",
    "do anything",
    "ignore rules",
    "ignore safety",
    "no matter what",
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
