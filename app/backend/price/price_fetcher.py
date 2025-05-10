import yfinance as yf
from datetime import datetime, timedelta

def get_stock_prices(symbol):
    try:
        # Calculate the date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Fetch data using yfinance
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        # If today is not included, fetch the current price
        if end_date.strftime('%Y-%m-%d') not in data.index.strftime('%Y-%m-%d').tolist():
            current_price = stock.info['currentPrice']
            print(f"Current price for {symbol} (live): {current_price}")

        # Print the fetched data
        for date, row in data.iterrows():
            print(f"{date.strftime('%Y-%m-%d')}: {row['Close']}")

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")


if __name__ == "__main__":
    symbol = input("Enter the stock symbol: ").strip().upper()
    get_stock_prices(symbol)
