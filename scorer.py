from __future__ import annotations
from models import AssetStats, RiskResult


def score_risk(stats: AssetStats) -> RiskResult:
    breakdown: dict[str, int] = {}
    score = 0

    # ── 1. Asset class (улучшено для crypto) ────────────────────
    if stats.asset_class == "crypto":
        cap = stats.market_cap or 0
        if cap > 500_000_000_000:
            class_pts = 25
        elif cap > 50_000_000_000:
            class_pts = 30
        else:
            class_pts = 40
    else:
        class_scores = {
            "stock": 20,
            "fund": 10,
            "etf": 5,
            "index": 3,
        }
        class_pts = class_scores.get(stats.asset_class, 15)

    score += class_pts
    breakdown["asset_class"] = class_pts

    # ── 2. Beta ────────────────────────────────────────────────
    beta = stats.beta or 1.0
    if beta > 2:
        beta_pts = 30
    elif beta > 1.5:
        beta_pts = 22
    elif beta > 1.2:
        beta_pts = 15
    elif beta > 1.0:
        beta_pts = 8
    elif beta < 0.7:
        beta_pts = -10
    else:
        beta_pts = 0

    score += beta_pts
    breakdown["beta"] = beta_pts

    # ── 3. Market cap ──────────────────────────────────────────
    cap = stats.market_cap or 0
    if cap == 0:
        cap_pts = 10
    elif cap < 300_000_000:
        cap_pts = 25
    elif cap < 2_000_000_000:
        cap_pts = 18
    elif cap < 10_000_000_000:
        cap_pts = 10
    elif cap < 100_000_000_000:
        cap_pts = 3
    else:
        cap_pts = -8

    # ETF бонус стабильности
    if stats.asset_class == "etf":
        cap_pts -= 5

    score += cap_pts
    breakdown["market_cap"] = cap_pts

    # ── 4. 52-week range ───────────────────────────────────────
    high, low = stats.week52_high, stats.week52_low
    if high and low and low > 0:
        r = (high - low) / low
        if r > 1:
            range_pts = 20
        elif r > 0.6:
            range_pts = 15
        elif r > 0.35:
            range_pts = 8
        elif r > 0.15:
            range_pts = 3
        else:
            range_pts = 0
    else:
        range_pts = 5

    score += range_pts
    breakdown["52w_range"] = range_pts

    # ── 5. Liquidity (НОВОЕ) ───────────────────────────────────
    vol = stats.volume or 0
    if vol < 1_000_000:
        liq_pts = 10
    elif vol < 10_000_000:
        liq_pts = 5
    else:
        liq_pts = 0

    score += liq_pts
    breakdown["liquidity"] = liq_pts

    # ── 6. Dividend ────────────────────────────────────────────
    div = stats.dividend_yield or 0
    if div > 0.05:
        div_pts = -15
    elif div > 0.02:
        div_pts = -8
    elif div > 0:
        div_pts = -3
    else:
        div_pts = 0

    score += div_pts
    breakdown["dividend"] = div_pts

    # ── 7. P/E ─────────────────────────────────────────────────
    pe = stats.pe_ratio
    if pe is not None:
        if pe < 0:
            pe_pts = 15
        elif pe > 100:
            pe_pts = 12
        elif pe > 50:
            pe_pts = 7
        elif pe > 30:
            pe_pts = 3
        else:
            pe_pts = 0
    else:
        pe_pts = 5

    score += pe_pts
    breakdown["pe_ratio"] = pe_pts

    # ── Final ──────────────────────────────────────────────────
    score = max(0, min(100, score))

    if score >= 55:
        level = "high"
    elif score >= 28:
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
    top = sorted(breakdown.items(), key=lambda x: abs(x[1]), reverse=True)[:2]
    names = {
        "asset_class": "asset type",
        "beta": "volatility",
        "market_cap": "size",
        "52w_range": "price swings",
        "liquidity": "liquidity",
        "dividend": "dividend",
        "pe_ratio": "valuation",
    }
    factors = " and ".join(names.get(f, f) for f, _ in top)

    tone = (
        "High risk asset with strong volatility."
        if level == "high"
        else "Moderate risk profile."
        if level == "medium"
        else "Relatively stable asset."
    )

    return f"{stats.symbol}: {score}/100 ({level}). Driven by {factors}. {tone}"
