import yfinance as yf

def get_timeseries(curr_symbol,start,end,interval):
    data = yf.download(tickers=curr_symbol,
        start=start,end=end,interval=interval
    )
    # Need to figure out, how to normalize the dataframe
    result = data.reset_index(level=2,col_level=2,drop=True)
    result = result[["Date", "Close"]]
    result = result.rename(columns={"Date": "date", "Close": "rate"})
    return result