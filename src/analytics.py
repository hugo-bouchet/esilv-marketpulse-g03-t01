"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    date_dict = dict(prices)
    return date_dict
    #raise NotImplementedError  # Owner: see team table


def align_series(instrument_prices, benchmark_prices):
    instrument_by_date = index_by_date(instrument_prices)
    benchmark_by_date = index_by_date(benchmark_prices)

    common_dates = []
    for date in instrument_by_date:
        if date in benchmark_by_date:
            common_dates.append(date)

    common_dates.sort()

    aligned_instrument = []
    aligned_benchmark = []
    for date in common_dates:
        aligned_instrument.append(instrument_by_date[date])
        aligned_benchmark.append(benchmark_by_date[date])

    return aligned_instrument, aligned_benchmark


def calculate_period_return(prices):
    if len(prices) == 0:
        raise ValueError("Prices length must me >= 1")
    
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])

    if first_close == 0:
        raise ValueError("First close cannot be 0.")

    return ((last_close / first_close) - 1.0) * 100.0


def calculate_base_100(prices):
    first_close = float(prices[0]["close"])
    return [float(row["close"]) / first_close * 100.0 for row in prices]

def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return
