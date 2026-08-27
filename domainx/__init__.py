"""
DomainX: Specialized Domain-Specific Multi-Agent Framework
Verticals: Legal, Medical, Supply Chain
"""

__version__ = "1.0.0"
__author__ = "DomainX Specialized Intelligence"

from domainx.agents.legal import LegalAgent
from domainx.agents.medical import MedicalAgent
from domainx.agents.supply_chain import SupplyChainAgent
from domainx.orchestration.router import DomainRouter

__all__ = ["LegalAgent", "MedicalAgent", "SupplyChainAgent", "DomainRouter"]
