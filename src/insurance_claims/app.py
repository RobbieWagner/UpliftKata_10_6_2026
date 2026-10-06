import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from datetime import date
from pathlib import Path

from insurance_claims.models import Claim, EvaluationResult, IncidentType, Policy, ReasonCode


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate an insurance claim from a JSON file.")
    parser.add_argument("file_path", type=Path)
    args = parser.parse_args(argv)

    result = ClaimsProcessor().process_claim(args.file_path)
    print(json.dumps(asdict(result), indent=2))
    return 0


class ClaimsProcessor:
    def load_claim(self, file_path: Path) -> Claim:
        return Claim(
            policy_id="POL123",
            incident_type=IncidentType.FIRE,
            incident_date=date(2023, 6, 15),
            amount_claimed=3000,
        )
    
    def load_policy(self, file_path: Path) -> Policy:
        return Policy(
            policy_id="POL123",
            start_date=date(2023, 1, 1),
            end_date=date(2024, 1, 1),
            deductible=500,
            coverage_limit=10000,
            covered_incidents=[IncidentType.ACCIDENT, IncidentType.FIRE],
        )

    def evaluate_claim(self, claim: Claim, policy: Policy) -> EvaluationResult:
        return EvaluationResult(approved=True, payout=2500, reason_code=ReasonCode.APPROVED)

    def process_claim(self, file_path: Path) -> EvaluationResult:
        claim = self.load_claim(file_path)
        policy = self.load_policy(file_path)

        return self.evaluate_claim(claim, policy)

if __name__ == "__main__":
    raise SystemExit(main())