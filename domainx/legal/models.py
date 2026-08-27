from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ClauseRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ContractType(str, Enum):
    MSA = "MSA"           # Master Services Agreement
    NDA = "NDA"           # Non-Disclosure Agreement
    SLA = "SLA"           # Service Level Agreement
    DPA = "DPA"           # Data Processing Agreement
    EMPLOYMENT = "EMPLOYMENT"

class Jurisdiction(str, Enum):
    US_DELAWARE = "US_DELAWARE"
    US_NEW_YORK = "US_NEW_YORK"
    UK_ENGLAND_WALES = "UK_ENGLAND_WALES"
    EU_GDPR = "EU_GDPR"
    UAE_DIFC = "UAE_DIFC"

class ClauseAudit(BaseModel):
    clause_title: str
    original_text: str
    risk_level: ClauseRiskLevel
    risk_rationale: str
    recommended_redline: str
    missing_protection_flag: bool = False

class ContractReviewRequest(BaseModel):
    contract_title: str
    contract_type: ContractType = ContractType.MSA
    governing_jurisdiction: Jurisdiction = Jurisdiction.US_DELAWARE
    contract_text: str
    party_representing: str = "Customer"

class ContractReviewResponse(BaseModel):
    contract_title: str
    contract_type: ContractType
    governing_jurisdiction: Jurisdiction
    overall_risk_score: float  # 0 to 100 (100 = critical risk)
    clauses_audited: List[ClauseAudit]
    key_liabilities_detected: List[str]
    favorable_terms_summary: str
    executive_legal_opinion: str
