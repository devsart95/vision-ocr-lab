from ocr_lab.domain import evaluate
from ocr_lab.publication import scan_text


def test_secret_signature_is_detected_without_embedding_a_real_credential() -> None:
    token = "sk-" + "or-v1-" + "a" * 64
    assert scan_text(token)
    assert scan_text("-" * 5 + "BEGIN " + "PRIVATE" + " KEY" + "-" * 5)
    assert not scan_text("OPENROUTER_API_KEY is read from the environment")


def test_invented_hidden_total_is_not_a_successful_abstention() -> None:
    score = evaluate({"total": None}, '{"total":"0"}')
    assert score["exact"] is False
    assert score["hallucinated_missing_fields"] == 1


def test_replay_is_a_dry_run_without_credentials() -> None:
    from pathlib import Path

    from ocr_lab.runner import replay

    assert replay(Path.cwd(), "01", "anthropic/claude-haiku-5.5", False) is None
