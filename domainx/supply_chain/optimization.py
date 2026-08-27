import math
from typing import List, Dict, Any
from domainx.supply_chain.models import SkuParameters, SkuOptimizationResult

# Z-score lookup for service level target
Z_SCORES = {
    90.0: 1.28,
    95.0: 1.645,
    98.0: 2.05,
    99.0: 2.33,
    99.9: 3.09
}

class InventoryOptimizationEngine:
    """
    Supply Chain Optimization Engine: Computes Economic Order Quantity (EOQ),
    Safety Stock (SS), Reorder Point (ROP), and Annual Policy Holding/Ordering costs.
    """

    @staticmethod
    def optimize_sku(sku: SkuParameters) -> SkuOptimizationResult:
        D = sku.annual_demand_units
        S = sku.order_cost_usd
        H = sku.holding_cost_per_unit_usd
        L = sku.supplier_lead_time_days
        sigma_d = sku.daily_demand_std_dev
        daily_demand = D / 365.0

        # 1. EOQ = sqrt( (2 * D * S) / H )
        eoq = math.sqrt((2.0 * D * S) / H) if H > 0 else D
        eoq_int = max(int(round(eoq)), 1)

        # 2. Safety Stock = Z * sigma_d * sqrt(LeadTime)
        z = Z_SCORES.get(sku.service_level_target_pct, 1.645)
        safety_stock = z * sigma_d * math.sqrt(L)
        ss_int = int(round(safety_stock))

        # 3. Reorder Point (ROP) = (DailyDemand * LeadTime) + SafetyStock
        rop = (daily_demand * L) + safety_stock
        rop_int = int(round(rop))

        # 4. Cost breakdown
        annual_holding = (eoq_int / 2.0 + ss_int) * H
        orders_per_year = D / eoq_int
        annual_ordering = orders_per_year * S
        total_policy_cost = annual_holding + annual_ordering

        # 5. Inventory turnover = Annual Demand / Average Inventory
        avg_inv = (eoq_int / 2.0) + ss_int
        turnover = round(D / avg_inv, 2) if avg_inv > 0 else 12.0

        return SkuOptimizationResult(
            sku_id=sku.sku_id,
            economic_order_quantity_eoq=eoq_int,
            reorder_point_units_rop=rop_int,
            safety_stock_units=ss_int,
            annual_holding_cost_usd=round(annual_holding, 2),
            annual_ordering_cost_usd=round(annual_ordering, 2),
            total_inventory_policy_cost_usd=round(total_policy_cost, 2),
            inventory_turnover_ratio=turnover,
            replenishment_orders_per_year=round(orders_per_year, 1)
        )
