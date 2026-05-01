from __future__ import annotations
from models import AssetStats, RiskResult
import math

HIGH_THRESHOLD = 60
MEDIUM_THRESHOLD = 30

WEIGHTS = {
    "asset_class": 0.20,
    "beta":        0.20,
    "market_cap":  0.15,
    "volatility":  0.20,
    "liquidity":   0.10,
    "valuation":   0.10,
    "dividend":    0.05,
}


def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))


def normalize_log(x, max_val):
    if x <= 0:
        return 100
    return clamp(100 * (1 - math.log(x + 1) / math.log(max_val + 1)))


def score_risk(stats: AssetStats) -> RiskResult:
    raw = {}

    class_base = {
        "crypto": 85,
        "stock":  50,
        "fund":   30,
        "etf":    20,
        "index":  10,
    }
    raw["asset_class"] = class_base.get(stats.asset_class, 50)

    beta = stats.beta if stats.beta is not None else 1.0
    raw["beta"] = clamp((beta - 0.7) * 60)

    cap = stats.market_cap or 0
    raw["market_cap"] = normalize_log(cap, 1_000_000_000_000)

    high, low = stats.week52_high, stats.week52_low
    if high and low and low > 0:
        r = (high - low) / low
        raw["volatility"] = clamp(r * 70)
    else:
        raw["volatility"] = 50

    vol = stats.volume or 0
    raw["liquidity"] = normalize_log(vol, 100_000_000)

    pe = stats.pe_ratio
    if pe is None:
        raw["valuation"] = 50
    elif pe < 0:
        raw["valuation"] = 85
    else:
        raw["valuation"] = clamp((pe / 40) * 50)

    div = stats.dividend_yield or 0
    if div > 0.08:
        raw["dividend"] = 40
    else:
        raw["dividend"] = clamp(60 - div * 800)

    score_float = sum(raw[f] * WEIGHTS[f] for f in WEIGHTS)
    score = int(clamp(round(score_float)))

    breakdown = {f: int(round(raw[f] * WEIGHTS[f])) for f in WEIGHTS}

    if score >= HIGH_THRESHOLD:
        level = "high"
    elif score >= MEDIUM_THRESHOLD:
        level = "medium"
    else:
        level = "low"

    summary = _build_summary(stats, level, score, breakdown)

    return RiskResult(
        symbol=stats.symbol,
        name=stats.name,
        price=stats.price,
        risk_level=level,
        risk_score=score,
        breakdown=breakdown,
        summary=summary,
    )


def _build_summary(stats, level, score, breakdown):
    top = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:2]
    names = {
        "asset_class": "asset type",
        "beta":        "market sensitivity",
        "market_cap":  "size",
        "volatility":  "price volatility",
        "liquidity":   "liquidity",
        "valuation":   "valuation",
        "dividend":    "dividend profile",
    }
    factors = " and ".join(names.get(f, f) for f, _ in top)
    tone = {
        "high":   "High risk — expect strong price swings.",
        "medium": "Moderate risk with balanced profile.",
        "low":    "Relatively stable asset.",
    }[level]
    return f"{stats.symbol}: {score}/100 ({level}). Driven by {factors}. {tone}"
