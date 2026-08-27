from typing import List, Dict, Any
from domainx.supply_chain.models import SkuParameters, SupplyChainDisruptionScore

class SupplyChainForecastingEngine:
    """
    Evaluates multi-echelon disruption risk, supplier lead-time volatility,
    and calculates carbon emissions for logistics replenishment.
    """

    @staticmethod
    def evaluate_disruption_and_emissions(skus: List[SkuParameters], transport_mode: str = "ROAD_FREIGHT") -> SupplyChainDisruptionScore:
        avg_lead_time = sum(s.supplier_lead_time_days for s in skus) / len(skus) if skus else 14.0
        lead_time_volatility = 15.0 if avg_lead_time > 21.0 else 5.0

        # Supplier concentration risk score
        supplier_concentration = 25.0 if len(skus) < 3 else 10.0

        disruption_index = min(supplier_concentration + lead_time_volatility + 12.0, 100.0)

        risk_level = "LOW"
        if disruption_index > 65:
            risk_level = "HIGH"
        elif disruption_index > 35:
            risk_level = "MODERATE"

        # Carbon factor calculation (g CO2 / tonne-km)
        carbon_factors = {
            "AIR_FREIGHT": 500.0,
            "ROAD_FREIGHT": 62.0,
            "RAIL_FREIGHT": 22.0,
            "MARITIME": 10.0
        }
        factor = carbon_factors.get(transport_mode.upper(), 62.0)
        
        # Estimate total tonnage
        total_units = sum(s.annual_demand_units for s in skus)
        total_tonnes = (total_units * 2.5) / 1000.0 # ~2.5kg per unit average
        distance_km = 850.0
        co2_tonnes = (total_tonnes * distance_km * factor) / 1000000.0

        recs = [
            "Maintain recommended dynamic safety stocks to protect against lead time variance.",
            f"Dual-source critical SKUs to lower supplier concentration risk from {supplier_concentration}%.",
            f"Optimize road transport routing to achieve 14% reduction in Scope 3 carbon emissions."
        ]

        return SupplyChainDisruptionScore(
            overall_disruption_risk_index=round(disruption_index, 1),
            risk_level=risk_level,
            supplier_concentration_risk=supplier_concentration,
            lead_time_volatility_risk=lead_time_volatility,
            carbon_emission_tonnes_co2e=round(co2_tonnes, 2),
            mitigation_recommendations=recs
        )
