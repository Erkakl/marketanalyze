# stock-risk-analyzer

Terminal tool that fetches **live market data** and scores each asset's risk — transparently, without black boxes.

No AI. Every point in the score is explainable.

---

## Demo

```
$ python main.py AAPL MSFT BTC-USD QQQ TSLA

Stock Risk Analyzer
Analyzing 5 asset(s): AAPL, MSFT, BTC-USD, QQQ, TSLA

────────────────────────────────────────────────────────
  BTC-USD    Bitcoin USD
  Price : $67,210.00
  Risk  : 🔴 HIGH     (score 76/100)

  Score breakdown:
    asset_class    +17  █████████████
    beta           +18  ██████████████
    market_cap      +6  ████
    volatility     +14  ███████████
    liquidity       +0  ·
    valuation       +5  ████
    dividend        +3  ██

  BTC-USD: 76/100 (high). Driven by market sensitivity and asset type. High risk — expect strong price swings.

════════════════════════════════════════════════════════
  SYMBOL      SCORE  RISK           PRICE
────────────────────────────────────────────────────────
  BTC-USD        76  🔴 high     $67,210.00
  TSLA           63  🔴 high       $172.30
  AAPL           34  🟡 medium     $170.45
  MSFT           31  🟡 medium     $424.46
  QQQ            17  🟢 low        $445.00
════════════════════════════════════════════════════════
```

---

## How it works

Each asset gets a **score from 0 to 100**. Every factor is scored 0–100 on a continuous scale, then multiplied by its weight.

| # | Factor | Weight | Logic |
|---|--------|--------|-------|
| 1 | Asset class | 20% | `crypto` > `stock` > `fund` > `etf` > `index` |
| 2 | Beta | 20% | Continuous scale — sensitivity to S&P 500 |
| 3 | Market cap | 15% | Log scale — micro-cap = more risk |
| 4 | Volatility | 20% | 52-week price range as % of low |
| 5 | Liquidity | 10% | Log scale — low volume = hard to exit |
| 6 | Valuation | 10% | P/E ratio — extreme values signal risk |
| 7 | Dividend | 5% | High yield = stable, no yield = speculative |

**Risk levels:**

| Score | Level |
|-------|-------|
| 0 – 29 | 🟢 Low |
| 30 – 59 | 🟡 Medium |
| 60 – 100 | 🔴 High |

---

## Install

```bash
git clone https://github.com/Erkakl/marketanalyze
cd marketanalyze
pip install -r requirements.txt
```

---

## Usage

**Interactive mode:**
```bash
python main.py
```
```
>> AAPL TSLA BTC-USD
>> NVDA
>> QUIT67
```

**CLI mode:**
```bash
python main.py AAPL MSFT BTC-USD
```

Exit with `QUIT67`.

---

## Project structure

```
stock-risk-analyzer/
├── main.py
├── fetcher.py
├── scorer.py
├── models.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Example results

| Symbol | Score | Level | Main drivers |
|--------|-------|-------|-------------|
| BTC-USD | 76 | 🔴 High | beta + volatility |
| TSLA | 63 | 🔴 High | beta + price swings |
| NVDA | 51 | 🟡 Medium | valuation (P/E) |
| AAPL | 34 | 🟡 Medium | asset type + size |
| QQQ | 17 | 🟢 Low | ETF + liquidity |
| BND | 9 | 🟢 Low | dividend + stability |

---

## Limitations

- Beta is historical — doesn't predict future volatility
- Crypto metrics are simplified
- ETF holdings not analyzed individually
- **Not financial advice**

---

## Future ideas

- `COMPARE AAPL MSFT` — side-by-side mode
- Export to JSON / CSV
- Web dashboard version

---

## License

MIT
