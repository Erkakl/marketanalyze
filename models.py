from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AssetStats:
    symbol: str
    name: str
    asset_class: str
    price: float
    beta: float | None
    market_cap: int | None
    week52_high: float | None
    week52_low: float | None
    dividend_yield: float | None
    pe_ratio: float | None
    volume: int | None


@dataclass
class RiskResult:
    symbol: str
    name: str
    price: float
    risk_level: str
    risk_score: int
    breakdown: dict[str, int]
    summary: str
