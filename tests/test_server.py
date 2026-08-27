from fastapi.testclient import TestClient
from domainx.server import app

client = TestClient(app)

def test_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_readyz():
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json()["specialized_domains_active"] == 3

def test_domains_list():
    res = client.get("/api/v1/domains")
    assert res.status_code == 200
    assert len(res.json()["domains"]) == 3

def test_api_legal():
    payload = {
        "contract_title": "MSA Cloud Services",
        "contract_type": "MSA",
        "governing_jurisdiction": "US_DELAWARE",
        "contract_text": "Limitation of liability is capped at 12 months fees. Mutual indemnification."
    }
    res = client.post("/api/v1/legal/review-contract", json=payload)
    assert res.status_code == 200
    assert "overall_risk_score" in res.json()

def test_api_medical():
    payload = {
        "encounter_id": "enc-test",
        "patient_age": 45,
        "gender": "M",
        "clinical_notes": "Patient Jane Doe DOB: 01/01/1980 with diabetes.",
        "active_medications": []
    }
    res = client.post("/api/v1/medical/code-encounter", json=payload)
    assert res.status_code == 200
    assert res.json()["hipaa_safe_harbor_compliant"] is True

def test_api_supply_chain():
    payload = {
        "facility_id": "DC-EAST",
        "skus": [{"sku_id": "SKU-A", "annual_demand_units": 4000, "order_cost_usd": 50, "holding_cost_per_unit_usd": 4}],
        "transport_mode": "ROAD_FREIGHT"
    }
    res = client.post("/api/v1/supply-chain/optimize-inventory", json=payload)
    assert res.status_code == 200
    assert res.json()["total_skus_optimized"] == 1
