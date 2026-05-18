"""Prompt quality analyzer."""

from __future__ import annotations

from typing import Any, Mapping, Optional

from promptclarity.metadata import analyze_metadata
from promptclarity.prompt_builder import build_improved_prompt
from promptclarity.recommender import missing_items_from_findings, recommendations_for
from promptclarity.risk import assess_risk
from promptclarity.rules import run_quality_rules, score_prompt, status_for_score
from promptclarity.types import GuardResult


class PromptClarity:
    """Validate prompts before they reach an LLM system."""

    def validate(
        self,
        prompt: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
        build_prompt: bool = True,
    ) -> GuardResult:
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        clean_prompt = prompt.strip()
        if not clean_prompt:
            raise ValueError("prompt cannot be empty")

        findings = run_quality_rules(clean_prompt)
        risk = assess_risk(clean_prompt)
        metadata_report = analyze_metadata(metadata)

        missing_items = missing_items_from_findings(findings)
        for item in metadata_report.missing_items:
            if item not in missing_items:
                missing_items.append(item)

        prompt_score = score_prompt(findings, risk.level)
        recommendations = recommendations_for(missing_items)
        finding_codes = {finding.code for finding in findings}
        if "vague_analyze" in finding_codes or "missing_analysis_type" in finding_codes:
            analysis_recommendations = [
                "Specify the type of analysis required.",
                "Mention whether you need EDA, prediction, reporting, or recommendations.",
            ]
            for recommendation in analysis_recommendations:
                if recommendation not in recommendations:
                    recommendations.append(recommendation)
        for recommendation in metadata_report.recommendations:
            if recommendation not in recommendations:
                recommendations.append(recommendation)

        status = status_for_score(prompt_score, risk.level)
        improved_prompt = (
            build_improved_prompt(clean_prompt, missing_items) if build_prompt else None
        )

        return GuardResult(
            status=status,
            prompt_score=prompt_score,
            risk_level=risk.level,
            missing_items=missing_items,
            recommendations=recommendations,
            findings=findings,
            improved_prompt=improved_prompt,
        )


PromptGuard = PromptClarity
