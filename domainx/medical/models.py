from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DiagnosticCode(BaseModel):
    code: str                  # e.g., E11.9
    code_system: str = "ICD-10-CM"
    description: str
    confidence_score: float = 0.99
    clinical_evidence: str

class ProcedureCode(BaseModel):
    code: str                  # e.g., 99214
    code_system: str = "CPT"
    description: str
    rvu_units: float = 1.92
    clinical_evidence: str

class DrugInteractionAlert(BaseModel):
    drug_a: str
    drug_b: str
    severity: str              # CONTRAINDICATED, MAJOR, MODERATE
    clinical_effect: str

class ClinicalEncounterRequest(BaseModel):
    encounter_id: str = "enc-001"
    patient_age: int = 54
    gender: str = "M"
    clinical_notes: str
    active_medications: List[str] = Field(default_factory=list)

class ClinicalEncounterResponse(BaseModel):
    encounter_id: str
    deidentified_clinical_notes: str
    hipaa_safe_harbor_compliant: bool = True
    diagnoses: List[DiagnosticCode]
    procedures: List[ProcedureCode]
    drug_interaction_alerts: List[DrugInteractionAlert]
    medical_necessity_verified: bool = True
    compliance_audit_id: str
