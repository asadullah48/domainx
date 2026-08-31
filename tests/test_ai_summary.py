from fastapi.testclient import TestClient

from domainx.ai.summarizer import ExecutiveSummaryEngine
from domainx.server import app

client = TestClient(app)

LEGAL_RESULT = {
    "overall_risk_score": 62,
    "clauses_audited": [
        {"clause_title": "Limitation of Liability", "risk_level": "CRITICAL"},
        {"clause_title": "Indemnification", "risk_level": "LOW"},
    ],
    "key_liabilities_detected": ["Uncapped consequential damages"],
    "executive_legal_opinion": "Recommend rejecting the uncapped liability clause.",
}

MEDICAL_RESULT = {
    "diagnoses": [{"code": "E11.9", "description": "Type 2 diabetes"}],
    "procedures": [{"code": "99214", "description": "Office visit"}],
    "drug_interaction_alerts": [
        {"drug_a": "Warfarin", "drug_b": "Aspirin", "severity": "MAJOR"}
    ],
}

SUPPLY_CHAIN_RESULT = {
    "total_skus_optimized": 1,
    "facility_id": "DC-EAST",
    "aggregate_holding_cost_savings_usd": 1234.5,
    "sku_replenishment_plans": [{"sku_id": "SKU-A"}],
    "disruption_analysis": {
        "overall_disruption_risk_index": 18.0,
        "risk_level": "LOW",
        "carbon_emission_tonnes_co2e": 0.42,
    },
}


def test_fallback_used_when_ollama_unreachable(monkeypatch):
    # Point at a loopback port nothing is listening on -> fast connection refusal,
    # exercising the real network failure path rather than mocking it away.
    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:65535")
    result = ExecutiveSummaryEngine.summarize("legal", LEGAL_RESULT)
    assert result["source"] == "fallback-template"
    assert "62/100" in result["summary"]
    assert "CRITICAL" in result["summary"] or "Limitation of Liability" in result["summary"]


def test_fallback_legal_mentions_score_and_opinion(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:65535")
    summary = ExecutiveSummaryEngine._fallback_summary("legal", LEGAL_RESULT)
    assert "62" in summary
    assert "uncapped liability" in summary.lower()


def test_fallback_medical_mentions_codes_and_alerts():
    summary = ExecutiveSummaryEngine._fallback_summary("medical", MEDICAL_RESULT)
    assert "E11.9" in summary
    assert "MAJOR" in summary
    assert "Warfarin" in summary


def test_fallback_medical_no_alerts_case():
    summary = ExecutiveSummaryEngine._fallback_summary("medical", {**MEDICAL_RESULT, "drug_interaction_alerts": []})
    assert "no drug-drug contraindications" in summary.lower()


def test_fallback_supply_chain_mentions_savings_and_risk():
    summary = ExecutiveSummaryEngine._fallback_summary("supply_chain", SUPPLY_CHAIN_RESULT)
    assert "DC-EAST" in summary
    assert "1,234.50" in summary
    assert "LOW" in summary


def test_fallback_unknown_domain():
    summary = ExecutiveSummaryEngine._fallback_summary("astrology", {})
    assert "astrology" in summary


def test_ollama_success_path_is_used_when_reachable(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": "This contract is high risk due to an uncapped liability clause."}

    def fake_post(url, json, timeout):
        assert url.endswith("/api/generate")
        return FakeResponse()

    monkeypatch.setattr("domainx.ai.summarizer.httpx.post", fake_post)
    result = ExecutiveSummaryEngine.summarize("legal", LEGAL_RESULT)
    assert result["source"].startswith("ollama:")
    assert "uncapped liability" in result["summary"].lower()


def test_ai_summarize_endpoint_returns_summary(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:65535")
    res = client.post("/api/v1/ai/summarize", json={"domain": "legal", "data": LEGAL_RESULT})
    assert res.status_code == 200
    body = res.json()
    assert body["domain"] == "legal"
    assert body["source"] == "fallback-template"
    assert len(body["summary"]) > 0
