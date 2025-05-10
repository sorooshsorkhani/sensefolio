# cli_tests/news_test_cli.py

from datetime import datetime
from app.backend.news.news_fetcher import company_news_finnhub

def main():
    print("📰 Sensefolio News Fetcher (CLI Test)")
    symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()

    news = company_news_finnhub(symbol, verbose=True)

    if not news:
        print("⚠️  No news found.")
        return

    print(f"\n📢 Top {min(5, len(news))} news headlines for {symbol}:\n")
    for article in news[:5]:
        headline = article.get("headline", "")
        url = article.get("url", "")
        timestamp = article.get("datetime", 0)
        pub_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

        print(f"- {pub_date} | {headline}")
        print(f"  {url}\n")

if __name__ == "__main__":
    main()
