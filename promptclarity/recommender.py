"""Recommendation generation for prompt gaps."""

from __future__ import annotations

from typing import Iterable, List

from promptclarity.types import RuleFinding


RECOMMENDATIONS = {
    "analysis type": "Specify the type of analysis required.",
    "business objective": "State the business objective or decision the answer should support.",
    "dataset details": "Describe the dataset, including source, fields, and size.",
    "output format": "Define the expected output format.",
    "quality target": "Explain what better means in measurable terms.",
    "success criteria": "Define the success criteria for a useful answer.",
    "task context": "Add enough task context for the model to understand the work.",
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
