import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any
from domainx.orchestration.router import DomainRouter
from domainx.legal.models import ContractReviewRequest
from domainx.medical.models import ClinicalEncounterRequest
from domainx.supply_chain.models import InventoryOptimizationRequest

app = FastAPI(
    title="DomainX Specialized Agent Framework Gateway",
    version="1.0.0",
    description="Domain-Specific Multi-Agent Platform outperforming generalist models across Legal, Medical, and Supply Chain verticals."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = DomainRouter()

class UnifiedDomainRequest(BaseModel):
    domain: str = Field(..., json_schema_extra={"example": "legal"})
    payload: Dict[str, Any]

@app.get("/healthz")
def healthz():
    return {"status": "healthy", "service": "DomainX", "version": "1.0.0"}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "specialized_domains_active": 3}

@app.get("/api/v1/domains")
def list_domains():
    return {
        "domains": [
            {"id": "legal", "agent": "LegalAgent", "specialty": "Contract Review & Redlining"},
            {"id": "medical", "agent": "MedicalAgent", "specialty": "ICD-10/CPT Coding & HIPAA Compliance"},
            {"id": "supply_chain", "agent": "SupplyChainAgent", "specialty": "EOQ, Safety Stock & Disruption Analytics"}
        ]
    }

@app.post("/api/v1/legal/review-contract")
def review_contract(req: ContractReviewRequest):
    return router.legal_agent.review_contract(req)

@app.post("/api/v1/medical/code-encounter")
def code_encounter(req: ClinicalEncounterRequest):
    return router.medical_agent.process_encounter(req)

@app.post("/api/v1/supply-chain/optimize-inventory")
def optimize_inventory(req: InventoryOptimizationRequest):
    return router.supply_chain_agent.optimize_inventory(req)

@app.post("/api/v1/domainx/analyze")
def unified_analyze(req: UnifiedDomainRequest):
    result = router.route_and_execute(req.domain, req.payload)
    if result.get("status") == "ERROR_UNKNOWN_DOMAIN":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
