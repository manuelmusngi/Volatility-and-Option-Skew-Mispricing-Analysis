import yfinance as yf

def fetch_historical_data(ticker, start_date, end_date):
    """Fetch historical price data for an asset."""
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def fetch_option_chain(ticker, expiration_date):
    """Fetch options chain data for a given stock ticker and expiration date."""
    stock = yf.Ticker(ticker)
    options = stock.option_chain(expiration_date)
    return options.calls, options.puts

# Example usage:
# data = fetch_historical_data('^SPX', '2023-01-01', '2023-12-31')
# calls, puts = fetch_option_chain('^SPX', '2023-06-16')
