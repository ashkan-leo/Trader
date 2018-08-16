import pandas as pd
import quandl

QUANDL_TOKEN = "ZUXueWCTcmEZRV7CAcBw"


def stock_data_quandl(ticker, start_date=None, end_date=None):
    if start_date and end_date:
        return quandl.get("WIKI/" + ticker, authtoken=QUANDL_TOKEN,
                          start_date=start_date, end_date=end_date)
    if start_date and not end_date:
        return quandl.get("WIKI/" + ticker, authtoken=QUANDL_TOKEN,
                          start_date=start_date)

    return quandl.get("WIKI/" + ticker, authtoken=QUANDL_TOKEN,
                      end_date=end_date)


def get_stocks(tickers, start_date=None, end_date=None):
    dataa = map(lambda t: stock_data_quandl(t, start_date, end_date), tickers)
    return pd.concat(dataa, keys=tickers, names=['Ticker', 'Date'])
