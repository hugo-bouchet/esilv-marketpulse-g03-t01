"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    date_dict = dict(prices)
    return date_dict
    #raise NotImplementedError  # Owner: see team table


def align_series(instrument_prices, benchmark_prices):
    raise NotImplementedError  # Owner: Lead


def calculate_period_return(prices):
    if len(prices) == 0:
        raise ValueError("Prices length must me >= 1")
    
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])

    if first_close == 0:
        raise ValueError("First close cannot be 0.")

    return ((last_close / first_close) - 1.0) * 100.0


def calculate_base_100(prices):
    raise NotImplementedError  # Owner: see team table


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError  # Owner: see team table
