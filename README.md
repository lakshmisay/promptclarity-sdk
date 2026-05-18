# PromptClarity SDK

Guard prompts before they become bad outputs.

PromptClarity SDK is a pre-LLM validation layer that detects unclear, incomplete, risky, or low-quality prompts before they reach an AI system.

## Positioning

PromptClarity SDK helps teams validate LLM inputs for:

- prompt quality scoring
- missing context detection
- ambiguity detection
- dataset metadata validation
- agent-readiness checks
- RAG-readiness checks
- cost and token waste reduction
- safer enterprise AI workflows

Enterprise tagline:

> A quality, clarity, and risk validation SDK for LLM inputs.

## Install

```bash
pip install promptclarity-sdk
```

## Usage

```python
from promptclarity import PromptClarity

guard = PromptClarity()

result = guard.validate("Analyze this data and give insights")

print(result.to_dict())
```

Example output:

```python
{
    "status": "needs_clarification",
    "prompt_score": 42,
    "risk_level": "low",
    "missing_items": [
        "success criteria",
        "dataset details",
        "business objective",
        "output format",
    ],
    "recommendations": [
        "Define the success criteria for a useful answer.",
        "Describe the dataset, including source, fields, and size.",
        "State the business objective or decision the answer should support.",
        "Define the expected output format.",
        "Specify the type of analysis required.",
        "Mention whether you need EDA, prediction, reporting, or recommendations.",
    ],
}
```

## Package Layout

```text
promptclarity/
|-- analyzer.py          # prompt quality analyzer
|-- rules.py             # rule-based checks
|-- risk.py              # unsafe / sensitive / vague input checks
|-- metadata.py          # dataset/file metadata analysis
|-- recommender.py       # missing-detail suggestions
|-- prompt_builder.py    # improved prompt generator
`-- __init__.py
```

## Development

```bash
python -m pytest
```

## Release Checklist

1. Update the version in `pyproject.toml` and `promptclarity/__init__.py`.
2. Run `python -m pytest`.
3. Build with `python -m build`.
4. Check the distribution with `python -m twine check dist/*`.
5. Upload to TestPyPI first, then PyPI.
