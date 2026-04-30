from __future__ import annotations

import time

from fetcher import fetch_stats
from scorer import score_risk


def print_result(r):
    print(f"\n{'─'*50}")
    print(f"{r.symbol} — {r.name}")
    print(f"Price: ${r.price:.2f}")
    print(f"Risk: {r.risk_level.upper()} ({r.risk_score}/100)")

    for k, v in r.breakdown.items():
        print(f"  {k:12}: {v:+}")

    print(r.summary)


def analyze(symbols):
    results = []

    for s in symbols:
        s = s.strip().upper()
        if not s:
            continue

        stats = fetch_stats(s)
        if not stats:
            continue

        result = score_risk(stats)
        results.append(result)
        print_result(result)

        time.sleep(0.5)


def main():
    print("\nStock Risk Analyzer (interactive mode)")
    print("Type tickers separated by space or comma")
    print("Type QUIT67 to exit\n")

    while True:
        raw = input(">> ").strip()

        # ── EXIT CONDITION ─────────────────────────────
        if raw.upper() == "QUIT67":
            print("Exiting...")
            break

        # ── PARSE INPUT ────────────────────────────────
        raw = raw.replace(",", " ")
        symbols = raw.split()

        if not symbols:
            print("No tickers entered")
            continue

        analyze(symbols)


if __name__ == "__main__":
    main()
