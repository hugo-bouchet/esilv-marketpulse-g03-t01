import yfinance as yf

CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}



def fetch_yahoo_prices(canonical_ticker, lookback, interval ) :
    yahoo_ticker = CANONICAL_TO_YAHOO[canonical_ticker]

    raw = yf.download(yahoo_ticker, period =lookback, interval =interval)

    raw.columns = raw.columns.get_level_values(0)

    rows = []
    for date, row in raw.iterrows():
        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    return rows
