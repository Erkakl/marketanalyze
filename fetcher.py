from __future__ import annotations

from typing import Any
import yfinance as yf

from models import AssetStats

QUOTE_TYPE_MAP = {
    "EQUITY":         "stock",
    "ETF":            "etf",
    "CRYPTOCURRENCY": "crypto",
    "MUTUALFUND":     "fund",
    "INDEX":          "index",
}


def fetch_stats(symbol: str) -> AssetStats | None:
    try:
        ticker = yf.Ticker(symbol)
        info: dict[str, Any] = ticker.info or {}

        if not info:
            print(f"  [!] No data for {symbol}")
            return None

        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("navPrice")
            or 0.0
        )

        raw_class = (info.get("quoteType") or "").upper()
        asset_class = QUOTE_TYPE_MAP.get(raw_class, "stock")

        return AssetStats(
            symbol=symbol.upper(),
            name=info.get("shortName") or info.get("longName") or symbol,
            asset_class=asset_class,
            price=float(price),
            beta=info.get("beta"),
            market_cap=info.get("marketCap"),
            week52_high=info.get("fiftyTwoWeekHigh"),
            week52_low=info.get("fiftyTwoWeekLow"),
            dividend_yield=(
                info.get("dividendYield")
                or info.get("trailingAnnualDividendYield")
            ),
            pe_ratio=info.get("trailingPE") or info.get("forwardPE"),
            volume=info.get("volume") or info.get("regularMarketVolume"),
        )

    except Exception as e:
        print(f"  [!] Error fetching {symbol}: {e}")
        return None
