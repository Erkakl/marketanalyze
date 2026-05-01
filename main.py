from __future__ import annotations

import sys
import time

from fetcher import fetch_stats
from scorer import score_risk

RISK_ICON = {
    "low":    "🟢",
    "medium": "🟡",
    "high":   "🔴",
}

BAR_CHAR = "█"
BAR_MAX = 15  # максимальная длина бара


def _bar(value: int, max_val: int = 25) -> str:
    """Визуальный бар пропорционально значению."""
    if value <= 0:
        return "·"
    length = max(1, round(value / max_val * BAR_MAX))
    return BAR_CHAR * min(length, BAR_MAX)


def print_result(r) -> None:
    icon = RISK_ICON.get(r.risk_level, "⚪")
    print(f"\n{'─' * 52}")
    print(f"  {r.symbol:<10} {r.name}")
    print(f"  Price : ${r.price:,.2f}")
    print(f"  Risk  : {icon} {r.risk_level.upper():<8} (score {r.risk_score}/100)")
    print()
    print("  Score breakdown:")
    for k, v in r.breakdown.items():
        bar = _bar(v)
        print(f"    {k:<14} {v:>+3}  {bar}")
    print()
    print(f"  {r.summary}")


def print_summary_table(results: list) -> None:
    if not results:
        return

    print(f"\n{'═' * 52}")
    print(f"  {'SYMBOL':<10} {'SCORE':>5}  {'RISK':<8}  {'PRICE':>12}")
    print(f"{'─' * 52}")

    for r in sorted(results, key=lambda x: x.risk_score, reverse=True):
        icon = RISK_ICON.get(r.risk_level, "⚪")
        print(
            f"  {r.symbol:<10} {r.risk_score:>5}  "
            f"{icon} {r.risk_level:<6}  ${r.price:>10,.2f}"
        )

    print(f"{'═' * 52}")


def analyze(symbols: list[str]) -> list:
    results = []

    for s in symbols:
        s = s.strip().upper()
        if not s:
            continue

        print(f"  Fetching {s}...")
        stats = fetch_stats(s)
        if not stats:
            continue

        result = score_risk(stats)
        results.append(result)
        print_result(result)

        time.sleep(0.5)

    return results


def main() -> None:
    # ── CLI режим: python main.py AAPL MSFT BTC-USD ───────────
    if len(sys.argv) > 1:
        symbols = [s.upper() for s in sys.argv[1:]]
        print(f"\nStock Risk Analyzer")
        print(f"Analyzing {len(symbols)} asset(s): {', '.join(symbols)}")
        results = analyze(symbols)
        print_summary_table(results)
        return

    # ── Интерактивный режим ────────────────────────────────────
    print("\nStock Risk Analyzer (interactive mode)")
    print("Type tickers separated by space or comma")
    print("Type QUIT67 to exit\n")

    session_results: list = []

    while True:
        try:
            raw = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not raw:
            continue

        if raw.upper() == "QUIT67":
            print("Exiting...")
            break

        # Поддержка запятых и пробелов как разделителей
        raw = raw.replace(",", " ")
        symbols = raw.split()

        if not symbols:
            print("No tickers entered")
            continue

        results = analyze(symbols)
        session_results.extend(results)

        # Показываем таблицу если было несколько тикеров
        if len(results) > 1:
            print_summary_table(results)


if __name__ == "__main__":
    main()
