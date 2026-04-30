# stock-risk-analyzer

A terminal tool that fetches **live market data** and scores each asset's risk level using a transparent, rule-based algorithm.

No AI. No black box. Every point in the score is explainable.

---

## Demo

```
$ python main.py AAPL MSFT BTC-USD QQQ TSM

Stock Risk Analyzer
Analyzing 5 asset(s): AAPL, MSFT, BTC-USD, QQQ, TSM

────────────────────────────────────────────────────────
  BTC-USD     Bitcoin USD
  Price : $67,210.00
  Risk  : HIGH    (score 72/100)

  Score breakdown:
    asset_class      +40  █████████████
    beta             +25  ████████
    market_cap       +10  ███
    52w_range        +15  █████
    dividend          +0  ·
    pe_ratio          +5  █

  BTC-USD scores 72/100 (high risk). Driven mainly by asset type and market volatility (beta).

────────────────────────────────────────────────────────
  AAPL        Apple Inc.
  Price : $170.45
  Risk  : MEDIUM  (score 31/100)

  Score breakdown:
    asset_class      +20  ██████
    beta             +15  █████
    market_cap        -8  ░░
    52w_range         +8  ██
    dividend          -3  ░
    pe_ratio          +3  █

  AAPL scores 31/100 (medium risk). Driven mainly by asset type and market volatility (beta).


════════════════════════════════════════════════════════
  SYMBOL      SCORE  RISK        PRICE
────────────────────────────────────────────────────────
  BTC-USD        72  high      $67,210.00
  TSM            45  medium      $393.83
  AAPL           31  medium      $170.45
  MSFT           28  medium      $424.46
  QQQ            18  low         $445.00
════════════════════════════════════════════════════════
```

---

## How it works

Each asset gets a **score from 0 to 100** based on 6 factors pulled directly from live market data.

| # | Factor | Max impact | Logic |
|---|--------|-----------|-------|
| 1 | Asset class | +40 | `crypto` > `stock` > `etf` — class alone signals baseline volatility |
| 2 | Beta | +30 / -10 | Measures how much the asset swings relative to the S&P 500 |
| 3 | Market cap | +25 / -8 | Micro-cap companies carry more risk than mega-cap blue chips |
| 4 | 52-week range | +20 | Wide price swings over the past year = historically volatile |
| 5 | Dividend yield | -15 | Dividend-paying companies tend to be mature and stable |
| 6 | P/E ratio | +15 | Extreme P/E signals speculative premium or negative earnings |

**Risk thresholds:**

| Score | Level |
|-------|-------|
| 0 – 27 | 🟢 Low |
| 28 – 54 | 🟡 Medium |
| 55 – 100 | 🔴 High |

---

## Project structure

```
stock-risk-analyzer/
│
├── main.py        # Entry point — terminal output, summary table
├── fetcher.py     # Pulls live data from Yahoo Finance via yfinance
├── scorer.py      # Rule-based risk scoring algorithm
├── models.py      # Data classes: AssetStats, RiskResult
│
├── requirements.txt
└── README.md
```
# stock-risk-analyzer

A terminal tool that fetches **live market data** and scores each asset's risk level using a transparent, rule-based algorithm.

No AI. No black box. Every point in the score is explainable.

Now supports **interactive mode** with continuous analysis and exit command `QUIT67`.

---

## Demo


$ python main.py
Stock Risk Analyzer (interactive mode)
Type tickers separated by space or comma
Type QUIT67 to exit

AAPL MSFT BTC-USD

──────────────────────────────────────────────
AAPL — Apple Inc.
Price: $170.45
Risk: MEDIUM (31/100)

asset_class : +20
beta : +15
market_cap : -8
52w_range : +8
liquidity : +5
dividend : -3
pe_ratio : +3

AAPL: 31/100 (medium). Moderate risk profile.

──────────────────────────────────────────────

QUIT67
Exiting...


---

## How it works

Each asset gets a **score from 0 to 100** based on live market data.

| # | Factor | Impact | Meaning |
|---|--------|--------|---------|
| 1 | Asset class | +40 | crypto > stock > ETF baseline risk |
| 2 | Beta | +30 / -10 | sensitivity to market movement |
| 3 | Market cap | +25 / -8 | size and stability |
| 4 | 52-week range | +20 | historical volatility |
| 5 | Liquidity (volume) | +10 | ease of entering/exiting |
| 6 | Dividend yield | -15 | stability signal |
| 7 | P/E ratio | +15 | valuation risk |

---

## Risk thresholds

| Score | Level |
|------|------|
| 0–27 | 🟢 Low |
| 28–54 | 🟡 Medium |
| 55–100 | 🔴 High |

---

## Features

### 🔄 Interactive mode
- Continuous analysis session
- Multiple tickers per input
- Exit with `QUIT67`

### 📊 Liquidity factor
- Low volume = higher risk
- Improves realism of scoring

### 📦 ETF handling
- Slightly reduced risk for diversification

---

## Project structure


stock-risk-analyzer/
├── main.py # interactive CLI engine
├── fetcher.py # Yahoo Finance data
├── scorer.py # risk scoring engine
├── models.py # data models
├── requirements.txt
└── README.md


---

## Install

```bash
git clone https://github.com/Erkakl/marketanalyze
cd marketanalize
pip install -r requirements.txt
Usage
Interactive mode (recommended)
python main.py

Then:

>> AAPL TSLA BTC-USD
>> NVDA
>> QUIT67
CLI mode (legacy)
python main.py AAPL MSFT BTC-USD
Example results
Symbol	Score	Level	Driver
BTC-USD	72	🔴 High	crypto volatility
TSLA	58	🔴 High	beta + swings
NVDA	52	🟡 Medium	valuation
AAPL	31	🟡 Medium	size + dividend
QQQ	18	🟢 Low	ETF diversification
BND	8	🟢 Low	bond stability
Why this matters

Most beginners look only at price.

This tool forces evaluation of:

volatility
liquidity
valuation
structural risk

It explains why an asset is risky, not just that it is.

Limitations
Beta is historical
Crypto metrics are simplified
ETF holdings not analyzed deeply
Not financial advice
Future ideas
compare mode (COMPARE AAPL MSFT)
export to JSON/CSV
volatility-based scoring
web dashboard version
License

MIT — use it freely, modify it, improve it.
