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

## Rule Coverage

PromptClarity currently uses 250+ deterministic rule signals across:

- vague prompt wording
- missing objective, audience, constraints, timeframe, examples, and success criteria
- dataset details and privacy handling
- output format and analysis type detection
- evaluation and selection criteria
- RAG source/citation readiness
- agent/tool boundary readiness
- sensitive-data patterns such as emails, phone numbers, SSNs, API keys, tokens, private keys, IPs, and cards
- unsafe-intent terms such as phishing, malware, prompt injection, SQL injection, credential theft, and bypass attempts

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

## Optional LLM Assistance

PromptClarity does not choose or bundle an LLM provider. By default, the SDK uses deterministic local rules only. If you want LLM-assisted semantic review, your application decides the model and passes an advisor callback.

```python
from promptclarity import PromptClarity


def my_llm_advisor(prompt, *, metadata=None):
    # Call your chosen model/provider here.
    # Return a dict or LLMReport.
    return {
        "model": "your-model-name",
        "confidence": 0.86,
        "missing_items": ["domain assumptions"],
        "recommendations": ["Clarify the assumptions the model should use."],
    }


guard = PromptClarity(llm_advisor=my_llm_advisor)
result = guard.validate("Analyze this data", use_llm=True)

print(result.to_dict())
```

Who decides the LLM?

- Your app decides the provider and model.
- PromptClarity decides the baseline rule-based score, status, and risk level.
- The optional LLM advisor adds extra missing items and recommendations.
- No LLM call happens unless `use_llm=True`.

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
|-- llm.py               # optional LLM advisor interface
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
