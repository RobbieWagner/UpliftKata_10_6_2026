from pathlib import Path

from insurance_claims import (ClaimsProcessor, EvaluationResult, ReasonCode)


def test_processes_happy_path_claim_from_json() -> None:
    json_dir = Path(__file__).parent / "json"
    processor = ClaimsProcessor()

    result = processor.process_claim(json_dir / "claim_and_policy.json")

    assert result == EvaluationResult(approved=True, payout=2500, reason_code=ReasonCode.APPROVED)