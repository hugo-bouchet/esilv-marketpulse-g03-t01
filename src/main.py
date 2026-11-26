from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    ACCESS_MODE as BLOOMBERG_ACCESS_MODE,
    fetch_bloomberg_prices,
)

# Active provider: "csv", "yahoo" or "bloomberg".
PROVIDER = "bloomberg"

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK = "1mo"
INTERVAL = "1d"
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

PROVIDER_LABELS = {
    "csv": "CSV",
    "yahoo": "Yahoo Finance",
    "bloomberg": "Bloomberg" if BLOOMBERG_ACCESS_MODE == "LIVE" else "Bloomberg stage",
}

ACCESS_MODES = {
    "csv": "LOCAL_FILE",
    "yahoo": "LIVE",
    "bloomberg": BLOOMBERG_ACCESS_MODE,
}


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def get_provider_rows(provider, instrument_ticker, benchmark_ticker):
    if provider == "bloomberg":
        return (
            fetch_bloomberg_prices(instrument_ticker),
            fetch_bloomberg_prices(benchmark_ticker),
        )

    if provider == "yahoo":
        # Imported here so that the other providers work without yfinance.
        from providers.yahoo_provider import fetch_yahoo_prices

        return (
            fetch_yahoo_prices(instrument_ticker, LOOKBACK, INTERVAL),
            fetch_yahoo_prices(benchmark_ticker, LOOKBACK, INTERVAL),
        )

    prices = load_prices()
    return (
        filter_prices(prices, instrument_ticker),
        filter_prices(prices, benchmark_ticker),
    )


def build_market_snapshot(provider=PROVIDER):
    """Shared application result for terminal (TD10) and Dash (TD11)."""
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices, benchmark_prices = get_provider_rows(
        provider, instrument["ticker"], benchmark["ticker"]
    )

    if not instrument_prices or not benchmark_prices:
        raise ValueError("Provider returned empty rows.")

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:
        raise ValueError("No common dates between instrument and benchmark.")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": PROVIDER_LABELS[provider],
        "access_mode": ACCESS_MODES[provider],
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
        "dates": [row["date"] for row in aligned_instrument],
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return, benchmark_return
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def display_market_summary(asset, prices, show_currency=True):
    currency = asset["currency"] if show_currency else ""

    print(asset["ticker"], "-", asset["name"])
    print("Market       :", asset["market"])
    print("Observations :", len(prices))
    print("First date   :", get_first_date(prices))
    print("Last date    :", get_last_date(prices))
    print("First close  :", get_first_close(prices), currency)
    print("Last close   :", get_last_close(prices), currency)


def display_comparison(snapshot):
    instrument_ticker = snapshot["instrument"]["ticker"]
    benchmark_ticker = snapshot["benchmark"]["ticker"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("Comparison (aligned)")
    print(f"Aligned sessions        : {len(snapshot['dates'])}")
    print(f"{instrument_ticker} period return      : {snapshot['instrument_return']:+.2f}%")
    print(f"{benchmark_ticker} period return     : {snapshot['benchmark_return']:+.2f}%")
    print(f"Relative performance    : {snapshot['relative_performance']:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument_ticker:<6} : {instrument_base_100[0]:.2f} -> {instrument_base_100[-1]:.2f}")
    print(f"{benchmark_ticker:<6} : {benchmark_base_100[0]:.2f} -> {benchmark_base_100[-1]:.2f}")


def main():
    snapshot = build_market_snapshot(PROVIDER)
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot["access_mode"])
    print()
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print()

    print("Instrument")
    display_market_summary(instrument, snapshot["instrument_prices"])
    print()
    print("Benchmark")
    display_market_summary(benchmark, snapshot["benchmark_prices"], show_currency=False)
    print()
    display_comparison(snapshot)


if __name__ == "__main__":
    main()