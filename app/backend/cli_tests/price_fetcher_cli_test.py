# app/backend/cli_tests/price_fetcher_cli_test.py

from app.backend.price.price_fetcher import fetch_historical_prices

def main():
    print("💹 Price Fetcher CLI Test")

    symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
    days_input = input("Enter number of days (default is 7): ").strip()

    try:
        days = int(days_input) if days_input else 7
    except ValueError:
        print("⚠️ Invalid number of days. Defaulting to 7.")
        days = 7

    prices = fetch_historical_prices(symbol=symbol, days=days, verbose=True)

    if not prices:
        print("⚠️ No price data returned.")
        return

    print(f"\n📊 Price Data for {symbol} (Last {days} Days):\n")
    for day in prices:
        print(
            f"{day['date']} | Open: {day['open']} | High: {day['high']} | "
            f"Low: {day['low']} | Close: {day['close']} | Volume: {day['volume']}"
        )

if __name__ == "__main__":
    main()
