// DomainX Specialized Multi-Agent Framework Studio Controller

let currentLang = 'en';

// Escapes text pulled from an API response before it is dropped into innerHTML.
// The AI summary can echo back user-submitted contract/clinical text (verbatim,
// via the LLM or the fallback templates), so it is untrusted for HTML purposes.
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}

// AI Executive Summary: narrates a deterministic agent result via the free-tier
// Ollama endpoint (with automatic template fallback server-side if unreachable).
async function renderAiSummary(boxId, domain, data) {
  const box = document.getElementById(boxId);
  if (!box) return;
  box.hidden = false;
  box.innerHTML = `
    <div class="ai-summary-header">
      <span class="ai-summary-title">🧠 AI Executive Briefing</span>
      <span class="ai-summary-source">generating…</span>
    </div>
    <p class="ai-summary-text">Narrating this result…</p>
  `;
  try {
    const res = await fetch('/api/v1/ai/summarize', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain, data })
    });
    const result = await res.json();
    box.innerHTML = `
      <div class="ai-summary-header">
        <span class="ai-summary-title">🧠 AI Executive Briefing</span>
        <span class="ai-summary-source">${escapeHtml(result.source || 'unknown')}</span>
      </div>
      <p class="ai-summary-text">${escapeHtml(result.summary || 'No summary available.')}</p>
    `;
  } catch (err) {
    box.innerHTML = `
      <div class="ai-summary-header">
        <span class="ai-summary-title">🧠 AI Executive Briefing</span>
      </div>
      <p class="ai-summary-text">Unavailable: ${escapeHtml(err.message)}</p>
    `;
  }
}

const i18n = {
  en: {
    brandTitle: "DomainX Studio",
    brandSub: "Specialized Vertical Multi-Agent Framework (Legal • Medical • Supply Chain)",
    statusPill: "Gateway Active (Port 8002)",
    langBtn: "🌐 العربية",
    kpiLegal: "Legal Intelligence",
    kpiMedical: "Clinical Coding & HIPAA",
    kpiSC: "Supply Chain Optimization",
    kpiHallucination: "Hallucination Rate",
    tabLegal: "⚖️ Legal Studio",
    tabMedical: "🏥 Medical & HIPAA Studio",
    tabSupplyChain: "📦 Supply Chain Simulator",
    tabRouter: "🔀 Unified Router Console",
    legalTitle: "⚖️ Legal Contract Review & Redlining",
    contractTitle: "Contract Title",
    contractType: "Agreement Type",
    jurisdiction: "Governing Jurisdiction",
    contractText: "Contract Clauses & Text",
    legalBtn: "🔍 Audit Contract & Generate Redlines",
    medTitle: "🏥 Clinical Coding & HIPAA Safe Harbor",
    clinicalNotes: "Clinical Encounter Notes (Unstructured)",
    medBtn: "🧪 Scrub PHI & Extract Diagnostic/CPT Codes",
    scTitle: "📦 Inventory Optimization & Disruption Simulator",
    scBtn: "🚀 Optimize Inventory & Disruption Model"
  },
  ar: {
    brandTitle: "استوديو DomainX المتخصص",
    brandSub: "إطار عمل الوكلاء متعددي التخصصات (القانوني • الطبي • سلاسل الإمداد)",
    statusPill: "البوابة السحابية نشطة (منفذ 8002)",
    langBtn: "🌐 English",
    kpiLegal: "الذكاء الاصطناعي القانوني",
    kpiMedical: "الترميز الطبي ومعايير HIPAA",
    kpiSC: "هندسة سلاسل الإمداد",
    kpiHallucination: "معدل الهلوسة في المراجع",
    tabLegal: "⚖️ الاستوديو القانوني",
    tabMedical: "🏥 الاستوديو الطبي وHIPAA",
    tabSupplyChain: "📦 محاكي سلاسل الإمداد",
    tabRouter: "🔀 موجه النطاقات الموحد",
    legalTitle: "⚖️ مراجعة العقود القانونية والتعديلات",
    contractTitle: "عنوان الاتفاقية / العقد",
    contractType: "نوع الاتفاقية",
    jurisdiction: "الاختصاص القضائي والقانون الحاكم",
    contractText: "نصوص وبنود العقد",
    legalBtn: "🔍 فحص العقد وتوليد التعديلات",
    medTitle: "🏥 الترميز الطبي وتطهير البيانات الصحية",
    clinicalNotes: "الملاحظات السريرية غير المهيكلة",
    medBtn: "🧪 تطهير البيانات واستخراج رموز ICD/CPT",
    scTitle: "📦 محاكي تحسين المخزون وانقطاع الإمداد",
    scBtn: "🚀 تحسين سياسات المخزون والانبعاثات"
  }
};

function switchTab(tabId) {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  
  const targetPane = document.getElementById(`tab-${tabId}`);
  if (targetPane) targetPane.classList.add('active');
  
  const btn = document.getElementById(`tab-btn-${tabId}`);
  if (btn) btn.classList.add('active');
}

function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'ar' : 'en';
  document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
  document.documentElement.lang = currentLang;

  const t = i18n[currentLang];
  document.getElementById('txt-brand-title').textContent = t.brandTitle;
  document.getElementById('txt-brand-sub').textContent = t.brandSub;
  document.getElementById('txt-status-pill').textContent = t.statusPill;
  document.getElementById('lang-btn-text').textContent = t.langBtn;
  document.getElementById('lbl-kpi-legal').textContent = t.kpiLegal;
  document.getElementById('lbl-kpi-medical').textContent = t.kpiMedical;
  document.getElementById('lbl-kpi-sc').textContent = t.kpiSC;
  document.getElementById('lbl-kpi-hallucination').textContent = t.kpiHallucination;
  
  document.getElementById('tab-btn-legal').textContent = t.tabLegal;
  document.getElementById('tab-btn-medical').textContent = t.tabMedical;
  document.getElementById('tab-btn-supplychain').textContent = t.tabSupplyChain;
  document.getElementById('tab-btn-router').textContent = t.tabRouter;

  document.getElementById('txt-legal-title').textContent = t.legalTitle;
  document.getElementById('lbl-contract-title').textContent = t.contractTitle;
  document.getElementById('lbl-contract-type').textContent = t.contractType;
  document.getElementById('lbl-jurisdiction').textContent = t.jurisdiction;
  document.getElementById('lbl-contract-text').textContent = t.contractText;
  document.getElementById('txt-legal-btn').textContent = t.legalBtn;

  document.getElementById('txt-med-title').textContent = t.medTitle;
  document.getElementById('lbl-clinical-notes').textContent = t.clinicalNotes;
  document.getElementById('txt-med-btn').textContent = t.medBtn;

  document.getElementById('txt-sc-title').textContent = t.scTitle;
  document.getElementById('txt-sc-btn').textContent = t.scBtn;
}

// 1. Legal Functions
function loadLegalPreset(type) {
  if (type === 'balanced') {
    document.getElementById('legal-text-input').value = `This Agreement contains a limitation of liability capped at the fees paid in the preceding twelve (12) months. Mutual indemnification applies for breach of confidentiality and IP infringement. Either party may terminate for convenience upon thirty (30) days written notice.`;
  } else if (type === 'risky') {
    document.getElementById('legal-text-input').value = `Neither party's liability shall be limited under this Agreement. Customer shall unilateral indemnify and defend Vendor against all third-party claims. Agreement shall remain in effect indefinitely without right of termination.`;
  }
}

async function executeLegalAudit() {
  const box = document.getElementById('legal-output-box');
  const badge = document.getElementById('legal-risk-badge');
  badge.textContent = "Auditing...";
  badge.className = "badge badge-purple";

  const payload = {
    contract_title: document.getElementById('legal-title-input').value,
    contract_type: document.getElementById('legal-type-select').value,
    governing_jurisdiction: document.getElementById('legal-jurisdiction-select').value,
    contract_text: document.getElementById('legal-text-input').value
  };

  try {
    const res = await fetch('/api/v1/legal/review-contract', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    const score = data.overall_risk_score;
    badge.textContent = `Risk Score: ${score}/100`;
    badge.className = score > 50 ? "badge badge-rose" : (score > 20 ? "badge badge-amber" : "badge badge-green");

    let clausesHtml = data.clauses_audited.map(c => `
      <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); padding:14px; border-radius:10px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <strong style="color:#fff;">${c.clause_title}</strong>
          <span class="badge ${c.risk_level === 'CRITICAL' ? 'badge-rose' : (c.risk_level === 'HIGH' ? 'badge-amber' : 'badge-green')}">${c.risk_level}</span>
        </div>
        <p style="font-size:0.85rem; color:#9ca3af; margin-bottom:6px;"><strong>Rationale:</strong> ${c.risk_rationale}</p>
        <p style="font-size:0.85rem; color:#6ee7b7; background:rgba(16,185,129,0.08); padding:8px; border-radius:6px;"><strong>Recommended Redline:</strong> ${c.recommended_redline}</p>
      </div>
    `).join('');

    box.innerHTML = `
      <div class="metric-summary-row">
        <div class="metric-tile">
          <div class="metric-tile-label">Overall Risk Score</div>
          <div class="metric-tile-val" style="color:${score > 50 ? 'var(--accent-rose)' : '#6ee7b7'}">${score}/100</div>
        </div>
        <div class="metric-tile">
          <div class="metric-tile-label">Clauses Audited</div>
          <div class="metric-tile-val">${data.clauses_audited.length}</div>
        </div>
        <div class="metric-tile">
          <div class="metric-tile-label">Critical Traps</div>
          <div class="metric-tile-val" style="color:var(--accent-rose);">${data.key_liabilities_detected.length}</div>
        </div>
      </div>
      <div style="margin-bottom:14px; padding:12px; background:rgba(168,85,247,0.08); border-radius:8px; font-size:0.86rem; color:#e9d5ff;">
        <strong>Executive Legal Opinion:</strong> ${data.executive_legal_opinion}
      </div>
      <h4 style="color:#fff; margin-bottom:10px; font-size:0.95rem;">Clause-by-Clause Findings:</h4>
      ${clausesHtml}
    `;
    renderAiSummary('legal-ai-box', 'legal', data);
  } catch (err) {
    box.innerHTML = `<div class="code-box" style="color:var(--accent-rose);">Error: ${err.message}</div>`;
  }
}

// 2. Medical Functions
function loadMedicalPreset(type) {
  if (type === 'diabetes') {
    document.getElementById('med-notes-input').value = `Patient: Jane Doe, DOB: 04/12/1966, SSN: 998-11-2233.
Assessment: 58-year-old female with uncontrolled type 2 diabetes and essential hypertension.
Ordered routine ECG and office visit for medication adjustment.`;
    document.getElementById('med-drugs-input').value = `Metformin 1000mg, Lisinopril 20mg`;
  } else if (type === 'lethal') {
    document.getElementById('med-notes-input').value = `Patient: John Q. Public, DOB: 01/15/1960, MRN: MRN-998822.
Assessment: Patient presenting with acute angina and chest pain.
Prescribed nitroglycerin sublingual.`;
    document.getElementById('med-drugs-input').value = `Nitroglycerin 0.4mg, Sildenafil 50mg, Warfarin 5mg, Aspirin 81mg`;
  }
}

async function executeMedicalAudit() {
  const box = document.getElementById('med-output-box');
  const badge = document.getElementById('med-badge');
  badge.textContent = "Processing...";
  badge.className = "badge badge-purple";

  const drugs = document.getElementById('med-drugs-input').value.split(',').map(s => s.trim()).filter(Boolean);
  const payload = {
    encounter_id: document.getElementById('med-enc-id').value,
    patient_age: 58,
    gender: "F",
    clinical_notes: document.getElementById('med-notes-input').value,
    active_medications: drugs
  };

  try {
    const res = await fetch('/api/v1/medical/code-encounter', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    badge.textContent = "HIPAA Compliant";
    badge.className = "badge badge-green";

    let diagBadges = data.diagnoses.map(d => `<span class="badge badge-cyan" style="margin-right:6px; margin-bottom:6px; display:inline-block;">${d.code} (${d.description})</span>`).join('');
    let procBadges = data.procedures.map(p => `<span class="badge badge-green" style="margin-right:6px; margin-bottom:6px; display:inline-block;">${p.code} (${p.description}) - RVU: ${p.rvu_units}</span>`).join('');
    
    let interactionAlerts = data.drug_interaction_alerts.map(a => `
      <div style="background:rgba(244,63,94,0.1); border:1px solid rgba(244,63,94,0.3); padding:12px; border-radius:8px; margin-bottom:8px;">
        <strong style="color:var(--accent-rose);">⚠️ ${a.severity}: ${a.drug_a} + ${a.drug_b}</strong>
        <p style="font-size:0.83rem; color:#fca5a5; margin-top:4px;">${a.clinical_effect}</p>
      </div>
    `).join('');

    box.innerHTML = `
      <div style="margin-bottom:14px;">
        <h4 style="color:#38bdf8; font-size:0.9rem; margin-bottom:6px;">🔒 De-Identified Clinical Notes (18 PHI Safe Harbor Redaction):</h4>
        <pre class="code-box" style="font-size:0.82rem; padding:10px;">${data.deidentified_clinical_notes}</pre>
      </div>

      <div style="margin-bottom:14px;">
        <h4 style="color:#6ee7b7; font-size:0.9rem; margin-bottom:6px;">🩺 Extracted ICD-10-CM Diagnostic Codes:</h4>
        <div>${diagBadges}</div>
      </div>

      <div style="margin-bottom:14px;">
        <h4 style="color:#a855f7; font-size:0.9rem; margin-bottom:6px;">💉 CPT Procedural Codes & Relative Value Units (RVU):</h4>
        <div>${procBadges}</div>
      </div>

      ${data.drug_interaction_alerts.length > 0 ? `
        <div>
          <h4 style="color:var(--accent-rose); font-size:0.9rem; margin-bottom:6px;">🚨 Drug-Drug Contraindication Alerts:</h4>
          ${interactionAlerts}
        </div>
      ` : `<p style="color:#6ee7b7; font-size:0.85rem;">✅ No high-risk drug-drug contraindications detected.</p>`}
    `;
    renderAiSummary('med-ai-box', 'medical', data);
  } catch (err) {
    box.innerHTML = `<div class="code-box" style="color:var(--accent-rose);">Error: ${err.message}</div>`;
  }
}

// 3. Supply Chain Functions
function calculateLiveSCPreview() {
  const D = parseFloat(document.getElementById('sc-demand').value) || 12000;
  const S = parseFloat(document.getElementById('sc-ordercost').value) || 85;
  const H = parseFloat(document.getElementById('sc-holdingcost').value) || 6.5;
  const L = parseFloat(document.getElementById('sc-leadtime').value) || 14;
  const sigma = parseFloat(document.getElementById('sc-stddev').value) || 4.5;
  const z = parseFloat(document.getElementById('sc-servicelevel').value) >= 99.0 ? 2.33 : 1.645;

  const eoq = Math.round(Math.sqrt((2 * D * S) / H));
  const ss = Math.round(z * sigma * Math.sqrt(L));
  const rop = Math.round((D / 365.0) * L + ss);

  const box = document.getElementById('sc-output-box');
  if (box.querySelector('.live-metric-row')) {
    document.getElementById('live-eoq').textContent = eoq;
    document.getElementById('live-ss').textContent = ss;
    document.getElementById('live-rop').textContent = rop;
  }
}

async function executeSupplyChainAudit() {
  const box = document.getElementById('sc-output-box');
  const badge = document.getElementById('sc-badge');
  badge.textContent = "Simulating...";
  badge.className = "badge badge-purple";

  const payload = {
    facility_id: document.getElementById('sc-facility').value,
    transport_mode: document.getElementById('sc-transport').value,
    skus: [
      {
        sku_id: document.getElementById('sc-skuid').value,
        annual_demand_units: parseFloat(document.getElementById('sc-demand').value),
        order_cost_usd: parseFloat(document.getElementById('sc-ordercost').value),
        holding_cost_per_unit_usd: parseFloat(document.getElementById('sc-holdingcost').value),
        supplier_lead_time_days: parseFloat(document.getElementById('sc-leadtime').value),
        daily_demand_std_dev: parseFloat(document.getElementById('sc-stddev').value),
        service_level_target_pct: parseFloat(document.getElementById('sc-servicelevel').value)
      }
    ]
  };

  try {
    const res = await fetch('/api/v1/supply-chain/optimize-inventory', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    const sku = data.sku_replenishment_plans[0];
    const dis = data.disruption_analysis;

    badge.textContent = "Optimization Complete";
    badge.className = "badge badge-green";

    box.innerHTML = `
      <div class="metric-summary-row live-metric-row">
        <div class="metric-tile">
          <div class="metric-tile-label">Optimal EOQ</div>
          <div id="live-eoq" class="metric-tile-val" style="color:var(--accent-cyan);">${sku.economic_order_quantity_eoq} units</div>
        </div>
        <div class="metric-tile">
          <div class="metric-tile-label">Safety Stock ($SS$)</div>
          <div id="live-ss" class="metric-tile-val" style="color:var(--accent-purple);">${sku.safety_stock_units} units</div>
        </div>
        <div class="metric-tile">
          <div class="metric-tile-label">Reorder Point ($ROP$)</div>
          <div id="live-rop" class="metric-tile-val" style="color:var(--accent-green);">${sku.reorder_point_units_rop} units</div>
        </div>
        <div class="metric-tile">
          <div class="metric-tile-label">Turnover Ratio</div>
          <div class="metric-tile-val">${sku.inventory_turnover_ratio}x</div>
        </div>
      </div>

      <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border-color); padding:16px; border-radius:10px; margin-bottom:14px;">
        <h4 style="color:#fff; margin-bottom:8px; font-size:0.92rem;">💰 Annual Policy Holding & Ordering Costs:</h4>
        <div style="display:flex; justify-content:space-between; font-size:0.86rem; color:#9ca3af; margin-bottom:4px;">
          <span>Annual Holding Cost:</span>
          <strong style="color:#fff;">$${sku.annual_holding_cost_usd}</strong>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.86rem; color:#9ca3af; margin-bottom:4px;">
          <span>Annual Ordering Setup Cost:</span>
          <strong style="color:#fff;">$${sku.annual_ordering_cost_usd}</strong>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.88rem; color:#6ee7b7; border-top:1px solid rgba(255,255,255,0.08); padding-top:6px; margin-top:4px;">
          <span>Estimated Annual Cost Savings:</span>
          <strong>$${data.aggregate_holding_cost_savings_usd}</strong>
        </div>
      </div>

      <div style="background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.2); padding:14px; border-radius:10px;">
        <h4 style="color:var(--accent-cyan); margin-bottom:6px; font-size:0.92rem;">🌍 Scope 1-3 Carbon & Disruption Radar:</h4>
        <p style="font-size:0.84rem; color:#bae6fd; margin-bottom:4px;">Transport Mode: <strong>${payload.transport_mode}</strong> • Estimated CO₂e: <strong>${dis.carbon_emission_tonnes_co2e} tonnes</strong></p>
        <p style="font-size:0.84rem; color:#bae6fd;">Disruption Risk Index: <strong>${dis.overall_disruption_risk_index}/100 (${dis.risk_level})</strong></p>
      </div>
    `;
    renderAiSummary('sc-ai-box', 'supply_chain', data);
  } catch (err) {
    box.innerHTML = `<div class="code-box" style="color:var(--accent-rose);">Error: ${err.message}</div>`;
  }
}

// 4. Router Functions
async function executeRouterDispatch() {
  const box = document.getElementById('router-output-box');
  const badge = document.getElementById('router-badge');
  badge.textContent = "Routing...";
  badge.className = "badge badge-purple";

  const domain = document.getElementById('router-domain-select').value;
  let payload = {};
  try {
    payload = JSON.parse(document.getElementById('router-payload-input').value);
  } catch(e) {
    payload = { text: document.getElementById('router-payload-input').value };
  }

  try {
    const res = await fetch('/api/v1/domainx/analyze', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain: domain, payload: payload })
    });
    const data = await res.json();
    badge.textContent = "Dispatched 200 OK";
    badge.className = "badge badge-green";
    box.innerHTML = `<pre class="code-box">${JSON.stringify(data, null, 2)}</pre>`;
  } catch (err) {
    box.innerHTML = `<div class="code-box" style="color:var(--accent-rose);">Router Error: ${err.message}</div>`;
  }
}
