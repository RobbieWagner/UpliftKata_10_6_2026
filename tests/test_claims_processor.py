from datetime import date
from pathlib import Path

from insurance_claims import (
    Claim,
    ClaimsProcessor,
    EvaluationResult,
    IncidentType,
    Policy,
    ReasonCode,
)


def test_loads_claim_from_json() -> None:
    json_file = Path(__file__).parent / "json" / "claim_and_policy.json"

    claim = ClaimsProcessor().load_claim(json_file)

    assert claim == Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )


def test_loads_policy_from_json() -> None:
    json_file = Path(__file__).parent / "json" / "claim_and_policy.json"

    policy = ClaimsProcessor().load_policy(json_file)

    assert policy == Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.ACCIDENT, IncidentType.FIRE],
    )


def test_processes_happy_path_claim_from_json() -> None:
    json_dir = Path(__file__).parent / "json"
    processor = ClaimsProcessor()

    result = processor.process_claim(json_dir / "claim_and_policy.json")

    assert result == EvaluationResult(approved=True, payout=2500, reason_code=ReasonCode.APPROVED)