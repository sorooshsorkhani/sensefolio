# stock_data_updated.py
# Updated module for fetching and visualizing stock data.

import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


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

        # Get the current price
        current_price = stock.info.get('currentPrice', None)

        return data, current_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None


def visualize_data(symbol, data, current_price):
    """
    Visualizes historical stock data and the current price.

    Args:
        symbol (str): The stock symbol.
        data (DataFrame): The historical stock data.
        current_price (float or None): The current stock price, if available.
    """
    if data is not None:
        plt.figure(figsize=(10, 6))

        # Plot historical prices
        plt.plot(
            data.index.strftime('%Y-%m-%d'),
            data['Close'],
            color='blue',
            marker='o',
            linestyle='-',
            label='Close Price'
            )

        # Check if current price exists and is not in historical data
        last_date = data.index[-1].strftime('%Y-%m-%d')
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_price is not None and current_date != last_date:
            plt.plot(
                [last_date, current_date],
                [data['Close'].iloc[-1], current_price],
                color='green' if current_price > data['Close'].iloc[-1] else 'red',
                linestyle='-',
                marker='o',
                label='Current Price'
                )

        # Set axis labels and title
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'Stock Price for {symbol}')
        plt.legend()

        plt.grid(True)
        plt.show()
    else:
        print(f"No data available to visualize for {symbol}.")


def main():
    """
    Main function to execute the script.
    """
    symbol = input("Enter the stock symbol (e.g., AAPL): ").strip().upper()
    data, current_price = get_data(symbol)

    # Visualize the data
    visualize_data(symbol, data, current_price)


if __name__ == "__main__":
    main()
