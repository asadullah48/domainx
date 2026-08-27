import pytest
from domainx.agents.legal import LegalAgent
from domainx.legal.models import ContractReviewRequest, ContractType, Jurisdiction, ClauseRiskLevel

def test_legal_contract_review_standard():
    agent = LegalAgent()
    req = ContractReviewRequest(
        contract_title="Vendor MSA 2026",
        contract_type=ContractType.MSA,
        governing_jurisdiction=Jurisdiction.US_DELAWARE,
        contract_text="""
        This Master Services Agreement contains a limitation of liability capped at the fees paid in the preceding twelve (12) months.
        Mutual indemnification applies for breach of confidentiality.
        Either party may terminate for convenience upon thirty (30) days written notice.
        """
    )
    res = agent.review_contract(req)
    assert res.overall_risk_score <= 25.0
    assert len(res.clauses_audited) >= 3
    assert "Delaware General Corporation Law" in res.executive_legal_opinion

def test_legal_contract_critical_risk():
    agent = LegalAgent()
    req = ContractReviewRequest(
        contract_title="Risky Vendor Agreement",
        contract_type=ContractType.MSA,
        governing_jurisdiction=Jurisdiction.UAE_DIFC,
        contract_text="""
        Neither party's liability shall be limited under this Agreement.
        Customer shall unilateral indemnify and defend Vendor against all claims.
        """
    )
    res = agent.review_contract(req)
    assert res.overall_risk_score >= 60.0
    critical_clauses = [c for c in res.clauses_audited if c.risk_level == ClauseRiskLevel.CRITICAL]
    assert len(critical_clauses) > 0
    assert "DIFC" in res.executive_legal_opinion
