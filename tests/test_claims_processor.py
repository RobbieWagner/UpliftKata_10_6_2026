from datetime import date
from pathlib import Path

import pytest

from insurance_claims import (
    Claim,
    ClaimsProcessor,
    IncidentType,
    Policy,
)
from insurance_claims.models import EvaluationResult, ReasonCode


def test_loads_claim_from_json() -> None:
    json_file = Path(__file__).parent / "json" / "claim.json"

    claim = ClaimsProcessor().load_claim(json_file)

    assert claim == Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )


def test_loads_policies() -> None:
    policies = ClaimsProcessor().load_policies()

    assert policies == [
        Policy(
            policy_id="POL123",
            start_date=date(2023, 1, 1),
            end_date=date(2024, 1, 1),
            deductible=500,
            coverage_limit=10000,
            covered_incidents=[IncidentType.ACCIDENT, IncidentType.FIRE],
        )
    ]


def test_get_policy_returns_matching_policy() -> None:
    claim = Claim(
        policy_id="POL456",
        incident_type=IncidentType.THEFT,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )
    matching_policy = Policy(
        policy_id="POL456",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=250,
        coverage_limit=5000,
        covered_incidents=[IncidentType.THEFT],
    )
    other_policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    policy = ClaimsProcessor().get_policy(claim, [other_policy, matching_policy])

    assert policy is matching_policy


def test_get_policy_raises_when_policy_is_not_found() -> None:
    claim = Claim(
        policy_id="UNKNOWN",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )

    with pytest.raises(LookupError):
        ClaimsProcessor().get_policy(claim, [])

def test_processes_happy_path_claim_from_json() -> None:
    json_dir = Path(__file__).parent / "json"
    processor = ClaimsProcessor()

    result = processor.process_claim(json_dir / "claim.json")

    assert result == EvaluationResult(approved=True, payout=2500, reason_code=ReasonCode.APPROVED)