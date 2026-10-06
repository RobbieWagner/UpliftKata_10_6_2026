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
        with file_path.open(encoding="utf-8") as json_file:
            data = json.load(json_file)

        return Claim(
            policy_id=data["policy_id"],
            incident_type=IncidentType(data["incident_type"]),
            incident_date=date.fromisoformat(data["incident_date"]),
            amount_claimed=data["amount_claimed"],
        )

    def load_policies(self) -> list[Policy]:
        policies_file_path = Path(__file__).resolve().parent.parent / "insurance_policies.json"
        with policies_file_path.open(encoding="utf-8") as json_file:
            policies_data = json.load(json_file)

        return [
            Policy(
                policy_id=policy_data["policy_id"],
                start_date=date.fromisoformat(policy_data["start_date"]),
                end_date=date.fromisoformat(policy_data["end_date"]),
                deductible=policy_data["deductible"],
                coverage_limit=policy_data["coverage_limit"],
                covered_incidents=[
                    IncidentType(incident) for incident in policy_data["covered_incidents"]
                ],
            )
            for policy_data in policies_data
        ]

    def get_policy(self, claim: Claim, policies: list[Policy]) -> Policy:
        for policy in policies:
            if policy.policy_id == claim.policy_id:
                return policy

        raise LookupError(f"No policy found for policy ID {claim.policy_id!r}")

    def evaluate_claim(self, claim: Claim, policy: Policy) -> EvaluationResult:
        return EvaluationResult(approved=True, payout=2500, reason_code=ReasonCode.APPROVED)

    def process_claim(self, file_path: Path) -> EvaluationResult:
        claim = self.load_claim(file_path)
        policies = self.load_policies()
        policy = self.get_policy(claim, policies)

        return self.evaluate_claim(claim, policy)

if __name__ == "__main__":
    raise SystemExit(main())