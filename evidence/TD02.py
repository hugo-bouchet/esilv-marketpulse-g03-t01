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