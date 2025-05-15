# stock_data.py
# Module responsible for stock_data from Yahoo! Finance.

import yfinance as yf
from datetime import datetime, timedelta

def get_data(symbol):
    """
    Fetches historical stock data and the current price if necessary.

    Args:
        symbol (str): The stock symbol to fetch data for.

    Returns:
        tuple: A tuple containing the historical data (DataFrame) and current price (float or None).
    """
    try:
        # Calculate the date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Fetch data using yfinance
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        # Check if current price needs to be fetched
        current_price = None
        if end_date.strftime('%Y-%m-%d') not in data.index.strftime('%Y-%m-%d').tolist():
            current_price = stock.info.get('currentPrice', None)

        return data, current_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None

def show_data(symbol, data, current_price):
    """
    Displays historical stock data and the current price.

    Args:
        symbol (str): The stock symbol.
        data (DataFrame): The historical stock data.
        current_price (float or None): The current stock price, if available.
    """
    if data is not None:
        # Display the fetched data
        print(f"\nHistorical prices for {symbol}:")
        for date, row in data.iterrows():
            print(f"{date.strftime('%Y-%m-%d')}: {row['Close']}")

        # Display the current price if available
        if current_price is not None:
            print(f"\nCurrent price for {symbol} (live): {current_price}")
    else:
        print(f"Failed to retrieve data for {symbol}.")

def main():
    """
    Main function to execute the script.
    """
    symbol = input("Enter the stock symbol: ").strip().upper()
    data, current_price = get_data(symbol)
    show_data(symbol, data, current_price)

if __name__ == "__main__":
    main()
