"""Rule-based prompt quality checks."""

from __future__ import annotations

import re
from typing import Iterable, List

from promptclarity.types import RuleFinding


VAGUE_TERMS = {
    "analyze": "analysis type",
    "check": "analysis type",
    "do analysis": "analysis type",
    "give me": "output format",
    "help me": "task context",
    "insights": "success criteria",
    "interesting": "success criteria",
    "key points": "success criteria",
    "this data": "dataset details",
    "the data": "dataset details",
    "my data": "dataset details",
    "some data": "dataset details",
    "better": "quality target",
    "best": "selection criteria",
    "good": "quality target",
    "nice": "quality target",
    "optimize": "optimization goal",
    "improve": "quality target",
    "report": "output format",
    "summary": "output format",
    "quickly": "time constraints",
    "as needed": "constraints",
    "etc": "task context",
    "stuff": "task context",
    "things": "task context",
    "everything": "scope",
    "all possible": "scope",
}

ANALYSIS_TERMS = {
    "ab test",
    "anomaly",
    "benchmark",
    "classification",
    "clustering",
    "cohort",
    "correlation",
    "diagnostic",
    "eda",
    "evaluation",
    "forecast",
    "hypothesis",
    "prediction",
    "ranking",
    "regression",
    "reporting",
    "root cause",
    "segmentation",
    "sentiment",
    "statistical",
    "summary",
    "trend",
}
OUTPUT_TERMS = {
    "api response",
    "bullet",
    "chart",
    "checklist",
    "csv",
    "dashboard",
    "diagram",
    "docstring",
    "email",
    "html",
    "json",
    "markdown",
    "paragraph",
    "plot",
    "presentation",
    "report",
    "schema",
    "slides",
    "sql",
    "table",
    "template",
    "text",
    "yaml",
}
OBJECTIVE_TERMS = {
    "business",
    "decision",
    "goal",
    "impact",
    "intent",
    "kpi",
    "metric",
    "objective",
    "outcome",
    "purpose",
    "success",
    "use case",
}
AUDIENCE_TERMS = {
    "audience",
    "beginner",
    "customer",
    "developer",
    "executive",
    "expert",
    "manager",
    "reader",
    "stakeholder",
    "technical",
    "user",
}
CONSTRAINT_TERMS = {
    "avoid",
    "budget",
    "constraint",
    "deadline",
    "do not",
    "limit",
    "must",
    "requirement",
    "should",
    "tone",
    "under",
    "within",
}
DATA_REFERENCE_TERMS = {
    "analytics",
    "csv",
    "data",
    "database",
    "dataset",
    "excel",
    "file",
    "jsonl",
    "log",
    "metrics",
    "records",
    "sheet",
    "spreadsheet",
    "table",
    "warehouse",
}
DATA_DETAIL_TERMS = {
    "columns",
    "database",
    "date range",
    "dictionary",
    "fields",
    "file",
    "format",
    "granularity",
    "labels",
    "rows",
    "sample",
    "schema",
    "source",
    "target",
    "time period",
    "types",
}
EVALUATION_TERMS = {
    "compare",
    "evaluate",
    "pick",
    "rank",
    "recommend",
    "review",
    "score",
    "select",
}
EVALUATION_CRITERIA_TERMS = {
    "accuracy",
    "baseline",
    "cost",
    "criteria",
    "f1",
    "latency",
    "metric",
    "precision",
    "recall",
    "rubric",
    "tradeoff",
}
EXAMPLE_REQUIRED_TERMS = {
    "classify",
    "convert",
    "extract",
    "format",
    "label",
    "parse",
    "rewrite",
    "transform",
}
EXAMPLE_TERMS = {"example", "few-shot", "sample", "input", "output", "expected"}
TIMEFRAME_TRIGGER_TERMS = {
    "current",
    "forecast",
    "historical",
    "latest",
    "recent",
    "trend",
    "today",
    "weekly",
    "yearly",
}
TIMEFRAME_TERMS = {
    "date",
    "date range",
    "day",
    "month",
    "period",
    "quarter",
    "timeframe",
    "timeline",
    "week",
    "year",
}
RAG_TERMS = {
    "context",
    "documents",
    "embedding",
    "knowledge base",
    "rag",
    "retrieval",
    "vector",
}
RAG_SOURCE_TERMS = {
    "citation",
    "document",
    "grounded",
    "page",
    "reference",
    "source",
    "url",
}
AGENT_TERMS = {
    "agent",
    "autonomous",
    "browser",
    "execute",
    "tool",
    "workflow",
}
AGENT_BOUNDARY_TERMS = {
    "approval",
    "boundary",
    "confirm",
    "permission",
    "policy",
    "rollback",
    "scope",
}
PRIVACY_TERMS = {
    "anonymize",
    "mask",
    "pii",
    "privacy",
    "redact",
    "sensitive",
}


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
            resolved_missing_item = missing_item
            if missing_item == "analysis type" and _contains_any(normalized, ANALYSIS_TERMS):
                resolved_missing_item = None
            if missing_item == "output format" and _contains_any(normalized, OUTPUT_TERMS):
                resolved_missing_item = None
            findings.append(
                RuleFinding(
                    code=f"vague_{term.replace(' ', '_')}",
                    message=f"Prompt uses vague wording: '{term}'.",
                    severity="medium",
                    missing_item=None if term == "analyze" else resolved_missing_item,
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

    if _mentions_data(normalized) and not _contains_any(normalized, PRIVACY_TERMS):
        findings.append(
            RuleFinding(
                code="missing_privacy_constraints",
                message="Prompt references data without privacy or sensitive-data handling instructions.",
                severity="medium",
                missing_item="privacy constraints",
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

    if _asks_for_content(normalized) and not _contains_any(normalized, AUDIENCE_TERMS):
        findings.append(
            RuleFinding(
                code="missing_audience",
                message="Prompt does not specify the intended audience.",
                severity="medium",
                missing_item="audience",
            )
        )

    if _asks_for_generation(normalized) and not _contains_any(normalized, CONSTRAINT_TERMS):
        findings.append(
            RuleFinding(
                code="missing_constraints",
                message="Prompt does not include constraints such as tone, length, deadline, or boundaries.",
                severity="medium",
                missing_item="constraints",
            )
        )

    if _contains_any(normalized, EVALUATION_TERMS) and not _contains_any(normalized, EVALUATION_CRITERIA_TERMS):
        findings.append(
            RuleFinding(
                code="missing_selection_criteria",
                message="Prompt asks for evaluation or recommendation without decision criteria.",
                severity="medium",
                missing_item="selection criteria",
            )
        )

    if _contains_any(normalized, EXAMPLE_REQUIRED_TERMS) and not _contains_any(normalized, EXAMPLE_TERMS):
        findings.append(
            RuleFinding(
                code="missing_examples",
                message="Prompt asks for transformation or extraction without examples.",
                severity="medium",
                missing_item="examples",
            )
        )

    if _contains_any(normalized, TIMEFRAME_TRIGGER_TERMS) and not _contains_any(normalized, TIMEFRAME_TERMS):
        findings.append(
            RuleFinding(
                code="missing_timeframe",
                message="Prompt references time-sensitive work without a timeframe.",
                severity="medium",
                missing_item="timeframe",
            )
        )

    if _contains_any(normalized, RAG_TERMS) and not _contains_any(normalized, RAG_SOURCE_TERMS):
        findings.append(
            RuleFinding(
                code="missing_rag_sources",
                message="Prompt references RAG or retrieval without source/citation requirements.",
                severity="medium",
                missing_item="retrieval sources",
            )
        )

    if _contains_any(normalized, AGENT_TERMS) and not _contains_any(normalized, AGENT_BOUNDARY_TERMS):
        findings.append(
            RuleFinding(
                code="missing_agent_boundaries",
                message="Prompt references agent or tool use without boundaries or approval rules.",
                severity="high",
                missing_item="agent boundaries",
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
    return _contains_any(text, DATA_DETAIL_TERMS) or bool(re.search(r"\b\d+\s*(rows|columns|records)\b", text))


def _mentions_data(text: str) -> bool:
    return _contains_any(text, DATA_REFERENCE_TERMS)


def _asks_for_content(text: str) -> bool:
    return _contains_any(
        text,
        {
            "blog",
            "create",
            "draft",
            "email",
            "explain",
            "generate",
            "message",
            "presentation",
            "report",
            "summarize",
            "write",
        },
    )


def _asks_for_generation(text: str) -> bool:
    return _contains_any(
        text,
        {
            "build",
            "create",
            "draft",
            "generate",
            "make",
            "plan",
            "prepare",
            "produce",
            "write",
        },
    )


def _normalize(prompt: str) -> str:
    return re.sub(r"\s+", " ", prompt.strip().lower())
