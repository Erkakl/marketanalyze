# stock-risk-analyzer

A terminal tool that fetches **live market data** and scores each asset's risk level using a transparent, rule-based algorithm.

No AI. No black box. Every point in the score is explainable.

Now supports **interactive mode** with continuous analysis and exit command `QUIT67`.

---

## Demo

```bash
$ python main.py
Stock Risk Analyzer (interactive mode)
Type tickers separated by space or comma
Type QUIT67 to exit

>> AAPL MSFT BTC-USD

──────────────────────────────────────────────
AAPL — Apple Inc.
Price: $170.45
Risk: MEDIUM (31/100)

asset_class : +20
beta        : +15
market_cap  : -8
52w_range   : +8
liquidity   : +5
dividend    : -3
pe_ratio    : +3

AAPL: 31/100 (medium). Moderate risk profile.

──────────────────────────────────────────────
>> QUIT67
Exiting...
```

## How it works

Each asset gets a score from 0 to 100 based on live market data.

#	Factor	Impact	Meaning
1	Asset class	+40	crypto > stock > ETF baseline risk
2	Beta	+30 / -10	sensitivity to market movement
3	Market cap	+25 / -8	size and stability
4	52-week range	+20	historical volatility
5	Liquidity (volume)	+10	ease of entering/exiting
6	Dividend yield	-15	stability signal
7	P/E ratio	+15	valuation risk

## Risk thresholds

| Score   | Level     |
|--------:|-----------|
| 0–27    | 🟢 Low     |
| 28–54   | 🟡 Medium  |
| 55–100  | 🔴 High    |

## Features
🔄 Interactive mode
Continuous analysis session
Multiple tickers per input
Exit with QUIT67
📊 Liquidity factor
Low volume = higher risk
Adds realism to scoring
📦 ETF handling
Slightly reduced risk due to diversification
## Project structure

stock-risk-analyzer/
├── main.py
├── fetcher.py
├── scorer.py
├── models.py
├── requirements.txt
└── README.md

## Install
```
git clone https://github.com/Erkakl/marketanalyze
cd marketanalyze
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
```
## Example results

| Symbol  | Score | Level       | Driver              |
|--------|------:|-------------|---------------------|
| BTC-USD | 72    | 🔴 High     | crypto volatility   |
| TSLA    | 58    | 🔴 High     | beta + swings       |
| NVDA    | 52    | 🟡 Medium   | valuation           |
| AAPL    | 31    | 🟡 Medium   | size + dividend     |
| QQQ     | 18    | 🟢 Low      | ETF diversification |
| BND     | 8     | 🟢 Low      | bond stability      |

## Why this matters

Most beginners look only at price.

This tool forces evaluation of:

volatility
liquidity
valuation
structural risk

It explains why an asset is risky, not just that it is.

## Limitations
Beta is historical
Crypto metrics are simplified
ETF holdings not deeply analyzed
Not financial advice

## Future ideas
compare mode (COMPARE AAPL MSFT)
export to JSON/CSV
volatility-based scoring
web dashboard version

## License

MIT — use it freely, modify it, improve it.
