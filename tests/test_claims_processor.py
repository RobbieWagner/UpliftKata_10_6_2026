from datetime import date
from pathlib import Path

import pytest

from insurance_claims import (
    Claim,
    ClaimsProcessor,
    EvaluationResult,
    IncidentType,
    Policy,
    ReasonCode,
)

# Loading tests


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


# Policy Decisioning Logic Tests


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


# Claim Approval/Denial Tests


def test_processes_happy_path_claim_from_json() -> None:
    json_dir = Path(__file__).parent / "json"
    processor = ClaimsProcessor()

    result = processor.process_claim(json_dir / "claim.json")

    assert result == EvaluationResult(approved=True, payout=2500, reason_code=ReasonCode.APPROVED)


@pytest.mark.parametrize("incident_date", [date(2022, 12, 31), date(2024, 1, 2)])
def test_claim_not_on_active_incident_date_denied(incident_date: date) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=incident_date,
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result == EvaluationResult(
        approved=False,
        payout=0,
        reason_code=ReasonCode.POLICY_INACTIVE,
    )

@pytest.mark.parametrize("incident_date", [date(2023, 1, 1)])
def test_claim_incident_date_on_policy_start_approved(incident_date: date) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=incident_date,
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=incident_date,
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)
    
    assert result == EvaluationResult(
        approved=True,
        payout=2500,
        reason_code=ReasonCode.APPROVED,
    )

@pytest.mark.parametrize("incident_date", [date(2024, 1, 1)])
def test_claim_incident_date_on_policy_end_approved(incident_date: date) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=incident_date,
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=incident_date,
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)
    
    assert result == EvaluationResult(
        approved=True,
        payout=2500,
        reason_code=ReasonCode.APPROVED,
    )

def test_claim_incident_not_in_covered_incidents_denied() -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.THEFT,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result == EvaluationResult(
        approved=False,
        payout=0,
        reason_code=ReasonCode.NOT_COVERED,
    )


def test_claim_with_empty_covered_incidents_list_denied() -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result == EvaluationResult(
        approved=False,
        payout=0,
        reason_code=ReasonCode.NOT_COVERED,
    )


@pytest.mark.parametrize("incident_type", list(IncidentType))
def test_claim_is_approved_for_each_supported_covered_incident_type(
    incident_type: IncidentType,
) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=incident_type,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=list(IncidentType),
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result == EvaluationResult(
        approved=True,
        payout=2500,
        reason_code=ReasonCode.APPROVED,
    )


@pytest.mark.parametrize("incident_type", list(IncidentType))
def test_claim_is_denied_when_its_type_is_missing_from_mixed_coverage(
    incident_type: IncidentType,
) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=incident_type,
        incident_date=date(2023, 6, 15),
        amount_claimed=3000,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[
            covered_type for covered_type in IncidentType if covered_type != incident_type
        ],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result == EvaluationResult(
        approved=False,
        payout=0,
        reason_code=ReasonCode.NOT_COVERED,
    )


@pytest.mark.parametrize("amount_claimed", [500, 400])
def test_claim_with_zero_or_negative_payout_returns_zero(
    amount_claimed: float,
) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=amount_claimed,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=500,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result == EvaluationResult(
        approved=False,
        payout=0,
        reason_code=ReasonCode.ZERO_PAYOUT,
    )



# Claim Payout Tests


@pytest.mark.parametrize(
    ("amount_claimed", "deductible", "expected_payout"),
    [
        (3000, 500, 2500),
        (1200, 200, 1000),
        (750.5, 50.25, 700.25),
        (100, 1, 99)
    ],
)
def test_payout_is_amount_claimed_minus_deductible(
    amount_claimed: float,
    deductible: float,
    expected_payout: float,
) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=amount_claimed,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=deductible,
        coverage_limit=10000,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result.approved is True
    assert result.payout == expected_payout
    assert result.reason_code is ReasonCode.APPROVED


@pytest.mark.parametrize(
    ("amount_claimed", "deductible", "limit", "expected_payout"),
    [
        (1000000, 10, 10, 10),
        (1200, 200, 1000, 1000),
        (750.5, 50.25, 100.1, 100.1),
        (750.5, 50.25, 700.25, 700.25),
    ],
)
def test_payout_doesnt_exceed_max(
    amount_claimed: float,
    deductible: float,
    limit: float,
    expected_payout: float,
) -> None:
    claim = Claim(
        policy_id="POL123",
        incident_type=IncidentType.FIRE,
        incident_date=date(2023, 6, 15),
        amount_claimed=amount_claimed,
    )
    policy = Policy(
        policy_id="POL123",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        deductible=deductible,
        coverage_limit=limit,
        covered_incidents=[IncidentType.FIRE],
    )

    result = ClaimsProcessor().evaluate_claim(claim, policy)

    assert result.approved is True
    assert result.payout == expected_payout
    assert result.reason_code is ReasonCode.APPROVED