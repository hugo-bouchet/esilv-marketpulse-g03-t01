import yfinance as yf

def fetch_yahoo_prices(canonical_ticker, lookback, interval ) :
    yahoo_ticker = ""
    if canonical_ticker == "AAPL" : 
        yahoo_ticker = "AAPL" 
    if canonical_ticker == "SP500" : 
        yahoo_ticker = "^GSPC"


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
