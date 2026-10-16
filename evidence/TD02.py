def get_last_close(filtered_prices):
    return float(filtered_prices[-1]["close"])


def get_first_close(filtered_prices):
    return float(filtered_prices[0]["close"])


def display_market_summary(asset, prices, show_currency=True):
    ticker = asset["ticker"]
    name = asset["name"]
    observations = len(prices)
    currency = asset["currency"]
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    print(ticker, "-", name)
    print("Observations :", observations)
    if show_currency:
        print("First close :", first_close, currency)
        print("Last close :", last_close, currency)
    else:
        print("First close :", first_close)
        print("Last close :", last_close)