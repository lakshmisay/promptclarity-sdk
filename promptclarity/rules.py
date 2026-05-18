"""Rule-based prompt quality checks."""

from __future__ import annotations

import re
from typing import Iterable, List

from promptclarity.types import RuleFinding


VAGUE_TERMS = {
    "analyze": "analysis type",
    "insights": "success criteria",
    "this data": "dataset details",
    "better": "quality target",
    "optimize": "optimization goal",
    "improve": "quality target",
    "report": "output format",
}

ANALYSIS_TERMS = {"eda", "prediction", "forecast", "classification", "summary", "reporting"}
OUTPUT_TERMS = {"json", "table", "markdown", "csv", "bullet", "dashboard", "chart"}
OBJECTIVE_TERMS = {"goal", "objective", "business", "decision", "use case", "success"}


def run_quality_rules(prompt: str) -> List[RuleFinding]:
    """Return deterministic quality findings for a prompt."""

    normalized = _normalize(prompt)
    findings: List[RuleFinding] = []

    if len(normalized.split()) < 8:
        findings.append(
            RuleFinding(
                code="too_short",
                message="Prompt is too short to contain enough task context.",
                severity="low",
            )
        )

    for term, missing_item in VAGUE_TERMS.items():
        if term in normalized:
            findings.append(
                RuleFinding(
                    code=f"vague_{term.replace(' ', '_')}",
                    message=f"Prompt uses vague wording: '{term}'.",
                    severity="medium",
                    missing_item=None if term == "analyze" else missing_item,
                )
            )

    if not _contains_any(normalized, OBJECTIVE_TERMS):
        findings.append(
            RuleFinding(
                code="missing_objective",
                message="Prompt does not state the business objective or decision goal.",
                severity="high",
                missing_item="business objective",
            )
        )

    if _mentions_data(normalized) and not _has_dataset_detail(normalized):
        findings.append(
            RuleFinding(
                code="missing_dataset_details",
                message="Prompt references data without describing the dataset.",
                severity="high",
                missing_item="dataset details",
            )
        )

    if not _contains_any(normalized, OUTPUT_TERMS):
        findings.append(
            RuleFinding(
                code="missing_output_format",
                message="Prompt does not define the expected output format.",
                severity="medium",
                missing_item="output format",
            )
        )

    if _mentions_data(normalized) and not _contains_any(normalized, ANALYSIS_TERMS):
        findings.append(
            RuleFinding(
                code="missing_analysis_type",
                message="Prompt does not specify the type of analysis required.",
                severity="medium",
            )
        )

    return _dedupe_findings(findings)


def score_prompt(findings: Iterable[RuleFinding], risk_level: str) -> int:
    """Calculate a 0-100 prompt quality score."""

    score = 100
    penalties = {"low": 5, "medium": 8, "high": 13}
    penalized_items = set()

    for finding in findings:
        if finding.missing_item:
            if finding.missing_item in penalized_items:
                continue
            penalized_items.add(finding.missing_item)
        score -= penalties.get(finding.severity, 8)

    risk_penalties = {"low": 0, "medium": 10, "high": 24}
    score -= risk_penalties.get(risk_level, 0)

    return max(0, min(100, score))


def status_for_score(score: int, risk_level: str) -> str:
    if risk_level == "high":
        return "blocked"
    if score < 60:
        return "needs_clarification"
    if score < 80:
        return "usable_with_warnings"
    return "ready"


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def _dedupe_findings(findings: Iterable[RuleFinding]) -> List[RuleFinding]:
    seen = set()
    result: List[RuleFinding] = []
    for finding in findings:
        key = (finding.code, finding.missing_item)
        if key not in seen:
            seen.add(key)
            result.append(finding)
    return result


def _has_dataset_detail(text: str) -> bool:
    detail_terms = {"columns", "rows", "schema", "fields", "csv", "database", "source", "file"}
    return _contains_any(text, detail_terms) or bool(re.search(r"\b\d+\s*(rows|columns|records)\b", text))


def _mentions_data(text: str) -> bool:
    return _contains_any(text, {"data", "dataset", "csv", "spreadsheet", "table", "database"})


def _normalize(prompt: str) -> str:
    return re.sub(r"\s+", " ", prompt.strip().lower())
