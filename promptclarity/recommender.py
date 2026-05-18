"""Recommendation generation for prompt gaps."""

from __future__ import annotations

from typing import Iterable, List

from promptclarity.types import RuleFinding


RECOMMENDATIONS = {
    "analysis type": "Specify the type of analysis required.",
    "agent boundaries": "Define tool-use boundaries, approvals, and actions the agent must not take.",
    "audience": "Specify the intended audience and their technical level.",
    "business objective": "State the business objective or decision the answer should support.",
    "constraints": "Add constraints such as tone, length, budget, deadline, or excluded actions.",
    "dataset details": "Describe the dataset, including source, fields, and size.",
    "examples": "Provide at least one input/output example.",
    "output format": "Define the expected output format.",
    "privacy constraints": "Explain how sensitive data should be masked, redacted, or avoided.",
    "quality target": "Explain what better means in measurable terms.",
    "retrieval sources": "Specify source, citation, or grounding requirements for retrieved context.",
    "scope": "Narrow the scope so the model knows what to include and exclude.",
    "selection criteria": "Define the criteria or metrics used to compare options.",
    "success criteria": "Define the success criteria for a useful answer.",
    "task context": "Add enough task context for the model to understand the work.",
    "time constraints": "Clarify timing expectations without relying on vague urgency.",
    "timeframe": "Specify the relevant date range or time period.",
}


def missing_items_from_findings(findings: Iterable[RuleFinding]) -> List[str]:
    items = []
    for finding in findings:
        if finding.missing_item and finding.missing_item not in items:
            items.append(finding.missing_item)
    return items


def recommendations_for(missing_items: Iterable[str]) -> List[str]:
    recommendations = []
    for item in missing_items:
        recommendation = RECOMMENDATIONS.get(item)
        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)

    return recommendations
