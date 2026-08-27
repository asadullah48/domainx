from typing import Dict, Any
from domainx.medical.models import ClinicalEncounterRequest, ClinicalEncounterResponse
from domainx.medical.coding_engine import MedicalCodingEngine
from domainx.medical.compliance import HIPAAComplianceScrubber

class MedicalAgent:
    """
    MedicalAgent: Specialized autonomous clinical coding and HIPAA compliance agent.
    Extracts ICD-10-CM / CPT codes and redacts all 18 HIPAA Safe Harbor identifiers.
    """
    def __init__(self, agent_id: str = "agent-medical-01"):
        self.agent_id = agent_id
        self.name = "MedicalAgent"
        self.version = "1.0.0"
        self.domain = "HEALTHCARE_AND_LIFE_SCIENCES"

    def process_encounter(self, request: ClinicalEncounterRequest) -> ClinicalEncounterResponse:
        deidentified = HIPAAComplianceScrubber.scrub_phi(request.clinical_notes)
        return MedicalCodingEngine.code_encounter(request, deidentified)
