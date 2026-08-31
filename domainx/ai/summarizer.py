"""
ExecutiveSummaryEngine: narrates DomainX's deterministic agent output as a
short, plain-English executive briefing.

Design principle: the deterministic engines (LegalAgent, MedicalAgent,
SupplyChainAgent) remain the single source of truth for every fact, score,
and code in a response -- that is DomainX's whole pitch versus a generalist
LLM. This layer never re-derives facts. It only *narrates* the structured
result it is handed, optionally through a locally-hosted, free-tier Ollama
model (https://ollama.com) when one is reachable.

If no Ollama daemon answers -- e.g. the public demo deployment, or a dev
machine without `ollama serve` running -- it falls back to a template-based
narrator built from the same structured fields, so the feature always
returns a real, honest answer instead of a blank state or a 502.
"""
import json
import os
from typing import Any, Dict, Optional

import httpx

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.2:1b"
DEFAULT_OLLAMA_TIMEOUT_SECONDS = 4.0


class ExecutiveSummaryEngine:
    @staticmethod
    def summarize(domain: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Return {"summary": str, "source": str} for the given domain result."""
        prompt = ExecutiveSummaryEngine._build_prompt(domain, data)
        llm_summary = ExecutiveSummaryEngine._try_ollama(prompt)
        if llm_summary:
            model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
            return {"summary": llm_summary, "source": f"ollama:{model}"}
        return {
            "summary": ExecutiveSummaryEngine._fallback_summary(domain, data),
            "source": "fallback-template",
        }

    @staticmethod
    def _build_prompt(domain: str, data: Dict[str, Any]) -> str:
        return (
            "You are an executive briefing assistant for DomainX, a specialized "
            f"enterprise multi-agent platform. Summarize the following {domain} "
            "analysis result in 3-4 concise sentences for a non-technical "
            "executive. Only state facts present in the JSON below -- never "
            "invent numbers, codes, or clauses that are not there.\n\n"
            f"JSON RESULT:\n{json.dumps(data, default=str)[:4000]}"
        )

    @staticmethod
    def _try_ollama(prompt: str) -> Optional[str]:
        host = os.environ.get("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)
        model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
        timeout = float(os.environ.get("OLLAMA_TIMEOUT_SECONDS", DEFAULT_OLLAMA_TIMEOUT_SECONDS))
        try:
            resp = httpx.post(
                f"{host}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=timeout,
            )
            resp.raise_for_status()
            text = resp.json().get("response", "").strip()
            return text or None
        except Exception:
            # Unreachable daemon, model not pulled, timeout, bad response shape --
            # any of these should degrade to the deterministic fallback, never 500.
            return None

    @staticmethod
    def _fallback_summary(domain: str, data: Dict[str, Any]) -> str:
        d = domain.lower().strip()
        if "legal" in d:
            return ExecutiveSummaryEngine._fallback_legal(data)
        if "medical" in d or "health" in d or "clinical" in d:
            return ExecutiveSummaryEngine._fallback_medical(data)
        if "supply" in d or "inventory" in d or "logistics" in d:
            return ExecutiveSummaryEngine._fallback_supply_chain(data)
        return (
            f"DomainX processed a '{domain}' request but no specialized narrator "
            "template is registered for this domain yet. Raw structured results "
            "are available in the response payload."
        )

    @staticmethod
    def _fallback_legal(data: Dict[str, Any]) -> str:
        score = data.get("overall_risk_score", "unknown")
        clauses = data.get("clauses_audited", []) or []
        critical = [c for c in clauses if c.get("risk_level") == "CRITICAL"]
        liabilities = data.get("key_liabilities_detected", []) or []
        lead = (
            f"This contract scored {score}/100 on DomainX's deterministic risk "
            f"scale across {len(clauses)} audited clause(s)."
        )
        if critical:
            lead += (
                f" {len(critical)} clause(s) were flagged CRITICAL, including: "
                f"{', '.join(c.get('clause_title', 'Untitled') for c in critical[:3])}."
            )
        if liabilities:
            lead += f" Key liability exposure: {'; '.join(liabilities[:2])}."
        opinion = data.get("executive_legal_opinion")
        if opinion:
            lead += f" Legal opinion: {opinion}"
        return lead

    @staticmethod
    def _fallback_medical(data: Dict[str, Any]) -> str:
        diagnoses = data.get("diagnoses", []) or []
        procedures = data.get("procedures", []) or []
        alerts = data.get("drug_interaction_alerts", []) or []
        lead = (
            f"Encounter coded to {len(diagnoses)} ICD-10-CM diagnosis code(s) and "
            f"{len(procedures)} CPT procedure code(s), with clinical notes "
            "de-identified under HIPAA Safe Harbor."
        )
        if diagnoses:
            lead += (
                " Diagnoses: "
                + ", ".join(f"{dx.get('code')} ({dx.get('description')})" for dx in diagnoses[:3])
                + "."
            )
        if alerts:
            lead += (
                f" {len(alerts)} drug-drug interaction alert(s) were raised, "
                f"most severe: {alerts[0].get('severity')} "
                f"({alerts[0].get('drug_a')} + {alerts[0].get('drug_b')})."
            )
        else:
            lead += " No drug-drug contraindications were detected."
        return lead

    @staticmethod
    def _fallback_supply_chain(data: Dict[str, Any]) -> str:
        plans = data.get("sku_replenishment_plans", []) or []
        savings = data.get("aggregate_holding_cost_savings_usd", 0)
        disruption = data.get("disruption_analysis", {}) or {}
        lead = (
            f"Optimized {data.get('total_skus_optimized', len(plans))} SKU(s) at "
            f"facility {data.get('facility_id', 'N/A')}, yielding an estimated "
            f"${savings:,.2f} in annual holding-cost savings versus naive ordering."
        )
        if disruption:
            lead += (
                f" Disruption risk index: {disruption.get('overall_disruption_risk_index')}/100 "
                f"({disruption.get('risk_level')}), with an estimated "
                f"{disruption.get('carbon_emission_tonnes_co2e')} tonnes CO2e for the shipment."
            )
        return lead
