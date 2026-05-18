"""Provider-agnostic hooks for optional LLM-assisted validation."""

from __future__ import annotations

from typing import Any, Callable, Mapping, Optional, Protocol, Union

from promptclarity.types import LLMReport


class LLMAdvisor(Protocol):
    """Callable interface for user-provided LLM prompt advisors."""

    def __call__(
        self,
        prompt: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Union[LLMReport, Mapping[str, Any]]:
        ...


def normalize_llm_report(report: Union[LLMReport, Mapping[str, Any]]) -> LLMReport:
    """Normalize an LLM advisor response into an LLMReport."""

    if isinstance(report, LLMReport):
        return report

    return LLMReport(
        missing_items=_as_string_list(report.get("missing_items", [])),
        recommendations=_as_string_list(report.get("recommendations", [])),
        confidence=_as_optional_float(report.get("confidence")),
        model=_as_optional_string(report.get("model")),
    )


def _as_optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_optional_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]
