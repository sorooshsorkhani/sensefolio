# app/backend/main.py
# CLI-style script to test fetching company news using the Finnhub API

from datetime import datetime
from app.backend.news.fetcher import company_news_finnhub

def main():
    """
    Prompts the user for a stock symbol and fetches the latest news
    using the company_news_finnhub function.
    """
    print("📈 Sensefolio News Fetcher (CLI Test)")
    symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()

    # Fetch news using default date range (last 7 days)
    news = company_news_finnhub(symbol=symbol, verbose=True)

    if not news:
        print("⚠️  No news found or an error occurred.")
        return

    print(f"\n📰 Latest news for {symbol}:\n")
    for article in news[:5]:  # Limit to top 5 articles
        # Convert Unix timestamp to human-readable date
        pub_date = datetime.fromtimestamp(article['datetime']).strftime('%Y-%m-%d')
        print(f"- {pub_date} | {article['headline']}")
        print(f"  {article['url']}\n")


if __name__ == "__main__":
    main()
