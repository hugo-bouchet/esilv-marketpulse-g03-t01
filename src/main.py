from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "CSV"


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]

def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_last_close(filtered_prices):
    return float(filtered_prices[-1]["close"])


def get_first_close(filtered_prices):
    return float(filtered_prices[0]["close"])

def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]



def display_market_summary(asset, prices, show_currency=True):
    ticker = asset["ticker"]
    name = asset["name"]
    market = asset["market"]
    observations = len(prices)
    currency = asset["currency"]
    first_date = get_first_date(prices)
    last_date = get_last_date(prices)
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    print(ticker, "-", name)
    print("Market :", market)
    print("Observations :", observations)
    print("First date :", first_date)
    print("Last date :", last_date)
    if show_currency:
        print("First close :", first_close, currency)
        print("Last close :", last_close, currency)
    else:
        print("First close :", first_close)
        print("Last close :", last_close)


def display_comparison(instrument, benchmark, instrument_prices, benchmark_prices):
    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative = calculate_relative_performance(instrument_return, benchmark_return)

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    instrument_ticker = instrument["ticker"]
    benchmark_ticker = benchmark["ticker"]

    print("Comparison (aligned)")
    print(f"Aligned sessions        : {len(aligned_instrument)}")
    print(f"{instrument_ticker} period return      : {instrument_return:+.2f}%")
    print(f"{benchmark_ticker} period return     : {benchmark_return:+.2f}%")
    print(f"Relative performance    : {relative:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument_ticker:<6} : {instrument_base_100[0]:.2f} -> {instrument_base_100[-1]:.2f}")
    print(f"{benchmark_ticker:<6} : {benchmark_base_100[0]:.2f} -> {benchmark_base_100[-1]:.2f}")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()

    print("Provider:", PROVIDER_LABEL)
    print()

    #print("Instrument")
    #print(f"{instrument['ticker']} - {instrument['name']}")
    #print(f"Last price: {instrument_latest['close']} {instrument['currency']}")
    #print()
    #print("Benchmark")
    #print(f"{benchmark['ticker']} - {benchmark['name']}")
    #print(f"Last level: {benchmark_latest['close']}")
    #print()
    #print(f"Period: {LOOKBACK_LABEL}")
    #print(f"Interval: {INTERVAL_LABEL}")
    #print()
    #print("Observations")
    #print(f"{instrument['ticker']}: {len(instrument_prices)}")
    #print(f"{benchmark['ticker']}: {len(benchmark_prices)}")


    print("Instrument")
    display_market_summary(instrument, instrument_prices)

    print()
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)

    print()
    display_comparison(instrument, benchmark, instrument_prices, benchmark_prices)


if __name__ == "__main__":
    main()
