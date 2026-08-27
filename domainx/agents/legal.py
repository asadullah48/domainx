from typing import Dict, Any
from domainx.legal.models import ContractReviewRequest, ContractReviewResponse
from domainx.legal.contract_engine import ContractReviewEngine

class LegalAgent:
    """
    LegalAgent: Specialized autonomous legal counsel agent.
    Performs contract review, clause risk scoring, liability cap analysis, and redline drafting.
    """
    def __init__(self, agent_id: str = "agent-legal-01"):
        self.agent_id = agent_id
        self.name = "LegalAgent"
        self.version = "1.0.0"
        self.domain = "LEGAL_AND_GOVERNANCE"

    def review_contract(self, request: ContractReviewRequest) -> ContractReviewResponse:
        return ContractReviewEngine.audit_contract(request)
