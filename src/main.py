from pathlib import Path
import csv
import json


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    row1 = prices[0]
    row2 = prices[1]
    close1 = row1["close"]
    close2 = row2["close"]
    f_close1 = float(close1)
    f_close2 = float(close2)
    return (f_close1, f_close2) 


def get_last_close(prices):
    row1 = prices[-1]
    row2 = prices[-2]
    close1 = row1["close"]
    close2 = row2["close"]
    f_close1 = float(close1)
    f_close2 = float(close2)
    return (f_close1, f_close2) 


def main():
    instruments = load_instruments()
    prices = load_prices()

    print(get_first_close(prices)[0])
    print(get_first_close(prices)[1])

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_latest['close']} {instrument['currency']}")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']}")
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Observations")
    print(f"{instrument['ticker']}: {len(instrument_prices)}")
    print(f"{benchmark['ticker']}: {len(benchmark_prices)}")


if __name__ == "__main__":
    main()
