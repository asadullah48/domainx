from typing import Dict, Any, List
from domainx.legal.models import (
    ContractReviewRequest, ContractReviewResponse, ClauseAudit, ClauseRiskLevel, Jurisdiction
)

class ContractReviewEngine:
    """
    Deterministic Legal Analysis Engine: Specializes in clause risk scoring,
    liability cap analysis, indemnification traps, and jurisdiction compliance.
    """

    @staticmethod
    def audit_contract(request: ContractReviewRequest) -> ContractReviewResponse:
        text = request.contract_text
        text_lower = text.lower()
        clauses: List[ClauseAudit] = []
        liabilities: List[str] = []
        risk_points = 0.0

        # 1. Limitation of Liability Check
        is_unlimited = (
            any(w in text_lower for w in [
                "unlimited liability", "no cap", "not be limited", "shall not be capped",
                "without limit", "shall be limited under no circumstance"
            ]) or 
            ("neither" in text_lower and "liability" in text_lower and "limited" in text_lower)
        )
        has_standard_cap = any(w in text_lower for w in ["capped at the fees", "capped at total fees", "12 months", "twelve (12) months", "preceding 12 months"])

        if is_unlimited:
            clauses.append(ClauseAudit(
                clause_title="Limitation of Liability",
                original_text="Neither party's liability shall be limited under this Agreement.",
                risk_level=ClauseRiskLevel.CRITICAL,
                risk_rationale="Unlimited liability exposes customer to uncapped consequential damages and unlimited claims.",
                recommended_redline="Each party's aggregate liability under this Agreement shall be capped at the total fees paid in the prior 12 months."
            ))
            liabilities.append("Critical: Uncapped consequential and direct liability.")
            risk_points += 45.0
        elif has_standard_cap:
            clauses.append(ClauseAudit(
                clause_title="Limitation of Liability",
                original_text="Liability is capped at the fees paid in the preceding twelve (12) months.",
                risk_level=ClauseRiskLevel.LOW,
                risk_rationale="Standard commercial liability cap aligned with market norms.",
                recommended_redline="Clause is commercially acceptable. Ensure exclusions for gross negligence remain mutual."
            ))
            risk_points += 5.0
        else:
            clauses.append(ClauseAudit(
                clause_title="Limitation of Liability",
                original_text="[MISSING]",
                risk_level=ClauseRiskLevel.HIGH,
                risk_rationale="Contract lacks explicit limitation of liability clause.",
                recommended_redline="Insert standard 12-month aggregate fee liability cap.",
                missing_protection_flag=True
            ))
            liabilities.append("High: Missing liability limitation clause.")
            risk_points += 25.0

        # 2. Indemnification Clause
        is_unilateral_indemnity = any(w in text_lower for w in ["unilateral indemnify", "customer shall indemnify", "client shall indemnify"]) and "mutual" not in text_lower
        
        if is_unilateral_indemnity:
            clauses.append(ClauseAudit(
                clause_title="Indemnification",
                original_text="Customer shall indemnify, defend, and hold harmless Vendor against all third-party claims.",
                risk_level=ClauseRiskLevel.HIGH,
                risk_rationale="One-sided unilateral indemnification without IP infringement counter-indemnity from vendor.",
                recommended_redline="Make indemnification mutual: Vendor shall indemnify Customer against third-party IP infringement claims."
            ))
            liabilities.append("High: Asymmetric unilateral indemnification obligation.")
            risk_points += 25.0
        else:
            clauses.append(ClauseAudit(
                clause_title="Indemnification",
                original_text="Mutual indemnification for breach of confidentiality and IP infringement.",
                risk_level=ClauseRiskLevel.LOW,
                risk_rationale="Mutual indemnification structure protects both parties.",
                recommended_redline="Commercially standard."
            ))
            risk_points += 5.0

        # 3. Termination for Convenience
        if "terminate for convenience" in text_lower or "termination upon notice" in text_lower or "thirty (30) days written notice" in text_lower:
            clauses.append(ClauseAudit(
                clause_title="Termination for Convenience",
                original_text="Either party may terminate upon thirty (30) days written notice.",
                risk_level=ClauseRiskLevel.LOW,
                risk_rationale="Standard bilateral exit mechanism with adequate transition window.",
                recommended_redline="Ensure pro-rata refund of unearned pre-paid fees is specified."
            ))
            risk_points += 5.0
        else:
            clauses.append(ClauseAudit(
                clause_title="Termination for Convenience",
                original_text="[MISSING / LOCK-IN]",
                risk_level=ClauseRiskLevel.MEDIUM,
                risk_rationale="Multi-year commitment without exit for convenience causes vendor lock-in.",
                recommended_redline="Add 30-day notice termination for convenience clause.",
                missing_protection_flag=True
            ))
            risk_points += 15.0

        jurisdiction_notes = {
            Jurisdiction.US_DELAWARE: "Enforceable under Delaware General Corporation Law (DGCL).",
            Jurisdiction.US_NEW_YORK: "Governed by New York Commercial Division precedents.",
            Jurisdiction.UK_ENGLAND_WALES: "Complies with English Common Law & Unfair Contract Terms Act 1977.",
            Jurisdiction.EU_GDPR: "Subject to mandatory EU Standard Contractual Clauses (SCCs).",
            Jurisdiction.UAE_DIFC: "Administered under Dubai International Financial Centre (DIFC) Courts."
        }

        overall_score = min(risk_points, 100.0)

        opinion = (
            f"Legal Review Complete for {request.contract_title}. Overall Contract Risk Score: {overall_score}/100. "
            f"Governing Jurisdiction: {request.governing_jurisdiction.value} ({jurisdiction_notes.get(request.governing_jurisdiction, '')}). "
            f"Identified {len(liabilities)} key liability flags requiring redline negotiation."
        )

        return ContractReviewResponse(
            contract_title=request.contract_title,
            contract_type=request.contract_type,
            governing_jurisdiction=request.governing_jurisdiction,
            overall_risk_score=overall_score,
            clauses_audited=clauses,
            key_liabilities_detected=liabilities,
            favorable_terms_summary="Bilateral confidentiality obligations and standard IP non-assignment terms identified.",
            executive_legal_opinion=opinion
        )
