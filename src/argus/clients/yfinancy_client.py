import yfinance as yf

def get_timeseries(curr_symbol,start,end,interval):
    data = yf.download(tickers=curr_symbol,
        start=start,end=end,interval=interval,multi_level_index=False,progress=False
    ) 
    if data is None:
        return None
    data = data.reset_index()
    data = data[["Date","Close"]]
    data = data.rename(columns={"Date": "date", "Close": "rate"})
    print(data.head())
    print(data.index)
    print(data.columns)
    # Need to figure out, how to normalize the dataframe
    #result = data.reset_index(level=2,col_level=2,drop=True)
    #result = result[["Date", "Close"]]
    #result = result.rename(columns={"Date": "date", "Close": "rate"})
    result = data.copy()
    return result