# Day 7 - Advanced Object-Oriented Frameworks & Institutional Contract Modeling
"""
Implements strict abstraction modeling, properties, classmethods, 
and advanced representation overrides mapping corporate financial parameters.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class TargetExecutionOrder:
    """Immutable data pattern representation protecting raw order parameters from inline contamination."""
    order_id: int
    symbol: str
    quantity: int
    limit_price: float

class FinancialInstrument(ABC):
    """Abstract baseline class establishing non-negotiable compliance protocols for derivative objects."""
    
    def __init__(self, asset_ticker: str, pricing_source: str) -> None:
        self._ticker = asset_ticker.upper()
        self._source = pricing_source
        
    @property
    def identity_ticker(self) -> str:
        """Secure read-only attribute container isolating symbol registry."""
        return self._ticker
        
    @abstractmethod
    def generate_regulatory_hash(self) -> Dict[str, Any]:
        """Forces all child components to implement explicit risk profile tracking matrices."""
        pass

class CashEquityAsset(FinancialInstrument):
    """Concrete child implementation representing traditional cash equity instruments."""
    
    TOTAL_REGISTERED_ASSETS = 0 # Class variable configuration
    
    def __init__(self, asset_ticker: str, pricing_source: str, underlying_sector: str) -> None:
        super().__init__(asset_ticker, pricing_source)
        self.sector = underlying_sector
        CashEquityAsset.TOTAL_REGISTERED_ASSETS += 1
        
    def generate_regulatory_hash(self) -> Dict[str, Any]:
        return {
            "AssetClass": "CashEquity",
            "TickerIdent": self._ticker,
            "SourceRoute": self._source,
            "SectorClassification": self.sector
        }
        
    @classmethod
    def read_registry_volume(cls) -> int:
        """Exposes systematic instantiation allocations to structural tracking entities."""
        return cls.TOTAL_REGISTERED_ASSETS

    def __repr__(self) -> str:
        return f"CashEquityAsset(Ticker={self._ticker}, Sector={self.sector})"

if __name__ == "__main__":
    print("--- Running Day 7 OOP Abstract Component Verification Engine ---")
    equity_security = CashEquityAsset("RELIANCE", "NSE_FEED_DIRECT", "Energy")
    print(equity_security)
    print(f"Regulatory Hash Mapping: {equity_security.generate_regulatory_hash()}")
    
    mock_order = TargetExecutionOrder(order_id=101, symbol="INFY", quantity=75, limit_price=1450.0)
    print(f"Immutable Dataclass Instantiated Cleanly: {mock_order}")
