from typing import Dict, Any
from domainx.supply_chain.models import (
    InventoryOptimizationRequest, InventoryOptimizationResponse
)
from domainx.supply_chain.optimization import InventoryOptimizationEngine
from domainx.supply_chain.forecasting import SupplyChainForecastingEngine

class SupplyChainAgent:
    """
    SupplyChainAgent: Specialized autonomous inventory and logistics optimization agent.
    Computes EOQ, Safety Stocks, Reorder Points, and disruption risk mitigation.
    """
    def __init__(self, agent_id: str = "agent-supplychain-01"):
        self.agent_id = agent_id
        self.name = "SupplyChainAgent"
        self.version = "1.0.0"
        self.domain = "LOGISTICS_AND_SUPPLY_CHAIN"

    def optimize_inventory(self, request: InventoryOptimizationRequest) -> InventoryOptimizationResponse:
        sku_results = [InventoryOptimizationEngine.optimize_sku(s) for s in request.skus]
        total_spend = sum(s.annual_demand_units * s.unit_purchase_price_usd for s in request.skus)
        
        # Calculate estimated holding cost savings vs naive ordering
        naive_holding = sum((s.annual_demand_units / 4.0) * s.holding_cost_per_unit_usd for s in request.skus)
        optimized_holding = sum(r.annual_holding_cost_usd for r in sku_results)
        savings = max(naive_holding - optimized_holding, 0.0)

        disruption = SupplyChainForecastingEngine.evaluate_disruption_and_emissions(
            request.skus, request.transport_mode
        )

        return InventoryOptimizationResponse(
            facility_id=request.facility_id,
            total_skus_optimized=len(sku_results),
            aggregate_annual_inventory_spend_usd=round(total_spend, 2),
            aggregate_holding_cost_savings_usd=round(savings, 2),
            sku_replenishment_plans=sku_results,
            disruption_analysis=disruption
        )
