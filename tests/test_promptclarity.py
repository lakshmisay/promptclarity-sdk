from promptclarity import PromptClarity, PromptGuard, __version__


def test_validate_flags_unclear_data_prompt():
    guard = PromptClarity()

    result = guard.validate("Analyze this data and give insights")

    assert result.status == "needs_clarification"
    assert result.prompt_score < 60
    assert result.risk_level == "low"
    assert "business objective" in result.missing_items
    assert "dataset details" in result.missing_items
    assert "output format" in result.missing_items
    assert "Specify the type of analysis required." in result.recommendations


def test_validate_ready_prompt_scores_high():
    guard = PromptClarity()

    result = guard.validate(
        "Create a markdown EDA summary for the customer churn dataset. "
        "The business objective is to identify retention actions. "
        "Use the csv file with 10000 rows and include success criteria. "
        "Write for executive stakeholders, redact sensitive fields, and keep it under 800 words."
    )

    assert result.status == "ready"
    assert result.prompt_score >= 80
    assert result.missing_items == []


def test_metadata_adds_dataset_recommendations():
    guard = PromptClarity()

    result = guard.validate(
        "Create a markdown EDA summary for the dataset with a business objective.",
        metadata={"name": "sales.csv"},
    )

    assert "columns" in result.missing_items
    assert "row count" in result.missing_items
    assert "source" in result.missing_items


def test_public_version_is_available():
    assert __version__ == "0.1.0"


def test_promptguard_alias_remains_available():
    assert PromptGuard is PromptClarity


def test_flags_agent_and_rag_readiness_gaps():
    guard = PromptClarity()

    result = guard.validate(
        "Build an autonomous RAG agent that uses tools to answer questions from context."
    )

    assert "agent boundaries" in result.missing_items
    assert "retrieval sources" in result.missing_items
    assert "Define tool-use boundaries" in " ".join(result.recommendations)


def test_flags_transformation_prompt_without_examples():
    guard = PromptClarity()

    result = guard.validate("Extract company names and dates from these records into JSON.")

    assert "examples" in result.missing_items
    assert "Provide at least one input/output example." in result.recommendations


def test_expanded_risk_patterns_detect_secret_and_attack_terms():
    guard = PromptClarity()

    result = guard.validate("Use password=abc123 to bypass login and test sql injection.")

    assert result.status == "blocked"
    assert result.risk_level == "high"
