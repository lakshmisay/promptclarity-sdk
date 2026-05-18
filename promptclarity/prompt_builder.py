"""Improved prompt generation."""

from __future__ import annotations

from typing import Iterable


def build_improved_prompt(original_prompt: str, missing_items: Iterable[str]) -> str:
    missing = list(missing_items)
    if not missing:
        return original_prompt.strip()

    lines = [original_prompt.strip(), "", "Please include:"]
    lines.extend(f"- {item}" for item in missing)
    return "\n".join(lines)

