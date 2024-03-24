import yfinance as yf

def get_latest_price_data(tickers):
    """Fetch the latest price data for a list of company tickers."""

    # Create an empty dictionary to store the price data
    price_data = {}
    
    # Fetch the latest price data for each company
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        latest_price = stock.history(period='1d')['Close'].iloc[-1]
        price_data[ticker] = latest_price
    
    return price_data