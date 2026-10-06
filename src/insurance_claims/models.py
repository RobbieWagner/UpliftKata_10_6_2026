from dataclasses import dataclass
from datetime import date
from enum import Enum


class IncidentType(str, Enum):
    ACCIDENT = "accident"
    THEFT = "theft"
    FIRE = "fire"
    WATER_DAMAGE = "water damage"


class ReasonCode(str, Enum):
    APPROVED = "APPROVED"
    POLICY_INACTIVE = "POLICY_INACTIVE"
    NOT_COVERED = "NOT_COVERED"
    ZERO_PAYOUT = "ZERO_PAYOUT"


@dataclass
class Claim:
    policy_id: str
    incident_type: IncidentType
    incident_date: date
    amount_claimed: float


@dataclass
class Policy:
    policy_id: str
    start_date: date
    end_date: date
    deductible: float
    coverage_limit: float
    covered_incidents: list[IncidentType]


@dataclass
class EvaluationResult:
    approved: bool
    payout: float
    reason_code: ReasonCode
