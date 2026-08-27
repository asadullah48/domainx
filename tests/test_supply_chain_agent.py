import pytest
from domainx.agents.supply_chain import SupplyChainAgent
from domainx.supply_chain.models import InventoryOptimizationRequest, SkuParameters

def test_inventory_eoq_and_disruption():
    agent = SupplyChainAgent()
    req = InventoryOptimizationRequest(
        facility_id="DC-CHICAGO-01",
        skus=[
            SkuParameters(
                sku_id="SKU-MICROCHIP-A1",
                annual_demand_units=10000.0,
                order_cost_usd=100.0,
                holding_cost_per_unit_usd=8.0,
                supplier_lead_time_days=21.0,
                daily_demand_std_dev=5.0,
                service_level_target_pct=95.0
            ),
            SkuParameters(
                sku_id="SKU-SENSOR-B2",
                annual_demand_units=5000.0,
                order_cost_usd=50.0,
                holding_cost_per_unit_usd=2.5,
                supplier_lead_time_days=10.0,
                daily_demand_std_dev=2.0,
                service_level_target_pct=98.0
            )
        ],
        transport_mode="ROAD_FREIGHT"
    )
    res = agent.optimize_inventory(req)
    assert res.total_skus_optimized == 2
    assert res.aggregate_holding_cost_savings_usd > 0
    assert len(res.sku_replenishment_plans) == 2
    
    # EOQ for SKU 1: sqrt((2 * 10000 * 100) / 8) = 500
    sku1 = res.sku_replenishment_plans[0]
    assert sku1.economic_order_quantity_eoq == 500
    assert sku1.safety_stock_units > 0
    assert sku1.reorder_point_units_rop > 0
    assert res.disruption_analysis.carbon_emission_tonnes_co2e > 0
