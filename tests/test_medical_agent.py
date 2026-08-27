import pytest
from domainx.agents.medical import MedicalAgent
from domainx.medical.models import ClinicalEncounterRequest

def test_medical_coding_and_hipaa():
    agent = MedicalAgent()
    req = ClinicalEncounterRequest(
        encounter_id="enc-9812",
        patient_age=58,
        gender="F",
        clinical_notes="""
        Patient: Jane Doe, DOB: 04/12/1966, SSN: 998-11-2233.
        Assessment: 58-year-old female with uncontrolled type 2 diabetes and essential hypertension.
        Ordered routine ECG and office visit for medication adjustment.
        """,
        active_medications=["Metformin 1000mg", "Lisinopril 20mg"]
    )
    res = agent.process_encounter(req)
    assert res.hipaa_safe_harbor_compliant is True
    # Verify PHI redacted
    assert "[REDACTED_NAME]" in res.deidentified_clinical_notes
    assert "[REDACTED_SSN]" in res.deidentified_clinical_notes
    
    # Verify Diagnostic Codes
    diag_codes = [d.code for d in res.diagnoses]
    assert "E11.9" in diag_codes  # Type 2 diabetes
    assert "I10" in diag_codes    # Hypertension
    
    # Verify Procedure Codes
    proc_codes = [p.code for p in res.procedures]
    assert "93000" in proc_codes or "99214" in proc_codes

def test_drug_interaction_detection():
    agent = MedicalAgent()
    req = ClinicalEncounterRequest(
        encounter_id="enc-interaction",
        clinical_notes="Patient with chest pain.",
        active_medications=["Warfarin 5mg", "Aspirin 81mg"]
    )
    res = agent.process_encounter(req)
    assert len(res.drug_interaction_alerts) > 0
    alert = res.drug_interaction_alerts[0]
    assert alert.severity == "MAJOR"
    assert "Warfarin" in alert.drug_a and "Aspirin" in alert.drug_b
