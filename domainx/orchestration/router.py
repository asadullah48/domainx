from typing import Dict, Any
from domainx.agents.legal import LegalAgent
from domainx.agents.medical import MedicalAgent
from domainx.agents.supply_chain import SupplyChainAgent
from domainx.legal.models import ContractReviewRequest
from domainx.medical.models import ClinicalEncounterRequest
from domainx.supply_chain.models import InventoryOptimizationRequest

class DomainRouter:
    """
    DomainX Router: Evaluates query intent and dispatches to the corresponding
    expert specialized agent, outperforming generalist models with deterministic rules.
    """
    def __init__(self):
        self.legal_agent = LegalAgent()
        self.medical_agent = MedicalAgent()
        self.supply_chain_agent = SupplyChainAgent()

    def route_and_execute(self, domain: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        d = domain.lower().strip()
        
        if "legal" in d or "contract" in d:
            req = ContractReviewRequest(**payload)
            res = self.legal_agent.review_contract(req)
            return {
                "status": "SUCCESS",
                "domain": "LEGAL",
                "agent_invoked": self.legal_agent.name,
                "data": res.model_dump()
            }
        elif "medical" in d or "health" in d or "clinical" in d:
            req = ClinicalEncounterRequest(**payload)
            res = self.medical_agent.process_encounter(req)
            return {
                "status": "SUCCESS",
                "domain": "MEDICAL",
                "agent_invoked": self.medical_agent.name,
                "data": res.model_dump()
            }
        elif "supply" in d or "inventory" in d or "logistics" in d:
            req = InventoryOptimizationRequest(**payload)
            res = self.supply_chain_agent.optimize_inventory(req)
            return {
                "status": "SUCCESS",
                "domain": "SUPPLY_CHAIN",
                "agent_invoked": self.supply_chain_agent.name,
                "data": res.model_dump()
            }
        else:
            return {
                "status": "ERROR_UNKNOWN_DOMAIN",
                "message": f"Domain '{domain}' not recognized. Supported domains: legal, medical, supply_chain."
            }
