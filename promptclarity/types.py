"""Typed result objects returned by PromptGuard."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class RuleFinding:
    """A single quality or clarity finding."""

    code: str
    message: str
    severity: str
    missing_item: Optional[str] = None


@dataclass(frozen=True)
class RiskReport:
    """Risk assessment for an LLM input."""

    level: str
    signals: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class MetadataReport:
    """Dataset or file metadata assessment."""

    missing_items: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class GuardResult:
    """Final validation response."""

    status: str
    prompt_score: int
    risk_level: str
    missing_items: List[str]
    recommendations: List[str]
    findings: List[RuleFinding] = field(default_factory=list)
    improved_prompt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

