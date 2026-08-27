from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SkuParameters(BaseModel):
    sku_id: str
    annual_demand_units: float = Field(..., description="Annual demand D")
    order_cost_usd: float = Field(default=50.0, description="Fixed order setup cost S")
    holding_cost_per_unit_usd: float = Field(default=5.0, description="Annual holding cost H")
    unit_purchase_price_usd: float = 25.0
    supplier_lead_time_days: float = 14.0
    daily_demand_std_dev: float = 4.0
    service_level_target_pct: float = 95.0

class SkuOptimizationResult(BaseModel):
    sku_id: str
    economic_order_quantity_eoq: int
    reorder_point_units_rop: int
    safety_stock_units: int
    annual_holding_cost_usd: float
    annual_ordering_cost_usd: float
    total_inventory_policy_cost_usd: float
    inventory_turnover_ratio: float
    replenishment_orders_per_year: float

class SupplyChainDisruptionScore(BaseModel):
    overall_disruption_risk_index: float  # 0 to 100
    risk_level: str                       # LOW, MODERATE, HIGH, SEVERE
    supplier_concentration_risk: float
    lead_time_volatility_risk: float
    carbon_emission_tonnes_co2e: float
    mitigation_recommendations: List[str]

class InventoryOptimizationRequest(BaseModel):
    facility_id: str = "DC-NORTH-AMERICA-01"
    skus: List[SkuParameters]
    transport_mode: str = "ROAD_FREIGHT"

class InventoryOptimizationResponse(BaseModel):
    facility_id: str
    total_skus_optimized: int
    aggregate_annual_inventory_spend_usd: float
    aggregate_holding_cost_savings_usd: float
    sku_replenishment_plans: List[SkuOptimizationResult]
    disruption_analysis: SupplyChainDisruptionScore
