from pathlib import Path

from insurance_claims.models import Claim, EvaluationResult, Policy


class ClaimsProcessor:
    def load_claim(self, file_path: Path) -> Claim:
        raise NotImplementedError

    def load_policy(self, file_path: Path) -> Policy:
        raise NotImplementedError

    def evaluate_claim(self, claim: Claim, policy: Policy) -> EvaluationResult:
        raise NotImplementedError

    def process_claim(self, file_path: Path) -> EvaluationResult:
        raise NotImplementedError