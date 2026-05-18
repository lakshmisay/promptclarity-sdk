"""Dataset and file metadata analysis."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from promptclarity.types import MetadataReport


REQUIRED_DATASET_FIELDS = {
    "name": "Name the dataset or file being analyzed.",
    "columns": "List important columns or fields.",
    "row_count": "Include row count or approximate size.",
    "source": "Mention where the dataset came from.",
}


def analyze_metadata(metadata: Optional[Mapping[str, Any]]) -> MetadataReport:
    if not metadata:
        return MetadataReport()

    missing: List[str] = []
    recommendations: List[str] = []

    for field, recommendation in REQUIRED_DATASET_FIELDS.items():
        if not metadata.get(field):
            missing.append(field.replace("_", " "))
            recommendations.append(recommendation)

    return MetadataReport(missing_items=missing, recommendations=recommendations)
