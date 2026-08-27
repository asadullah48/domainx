import pytest
from domainx.orchestration.router import DomainRouter

def test_router_legal():
    router = DomainRouter()
    res = router.route_and_execute("legal", {
        "contract_title": "NDA Test",
        "contract_text": "Mutual confidentiality agreement with limitation of liability."
    })
    assert res["status"] == "SUCCESS"
    assert res["domain"] == "LEGAL"
    assert res["agent_invoked"] == "LegalAgent"

def test_router_medical():
    router = DomainRouter()
    res = router.route_and_execute("medical", {
        "encounter_id": "enc-101",
        "clinical_notes": "Patient with hypertension diagnosis."
    })
    assert res["status"] == "SUCCESS"
    assert res["domain"] == "MEDICAL"
    assert res["agent_invoked"] == "MedicalAgent"

def test_router_supply_chain():
    router = DomainRouter()
    res = router.route_and_execute("supply_chain", {
        "facility_id": "DC-01",
        "skus": [{"sku_id": "SKU-1", "annual_demand_units": 1200, "order_cost_usd": 20, "holding_cost_per_unit_usd": 2}]
    })
    assert res["status"] == "SUCCESS"
    assert res["domain"] == "SUPPLY_CHAIN"
    assert res["agent_invoked"] == "SupplyChainAgent"

def test_router_unknown():
    router = DomainRouter()
    res = router.route_and_execute("cryptocurrency", {})
    assert res["status"] == "ERROR_UNKNOWN_DOMAIN"
