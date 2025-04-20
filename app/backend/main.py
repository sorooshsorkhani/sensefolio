# app/backend/main.py
# CLI-style script to test fetching company news using the Finnhub API
# Now includes sentiment analysis using VADER

from datetime import datetime
from app.backend.news.fetcher import company_news_finnhub
from app.backend.sentiment.sentiment_analyzer import SentimentAnalyzer


def main():
    """
    Prompts the user for a stock symbol, fetches recent news headlines,
    and analyzes the sentiment of each headline.
    """
    print("📈 Sensefolio News Sentiment Analyzer (CLI Test)")
    symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()

    # Fetch news using default date range (last 7 days)
    news = company_news_finnhub(symbol=symbol, verbose=True)

    if not news:
        print("⚠️  No news found or an error occurred.")
        return

    # Initialize the sentiment analyzer (default model: VADER)
    analyzer = SentimentAnalyzer()

    print(f"\n📰 Latest news for {symbol} with sentiment scores:\n")

    for article in news[:5]:  # Limit to top 5 articles
        headline = article.get("headline", "")
        url = article.get("url", "")
        timestamp = article.get("datetime", 0)

        # Convert Unix timestamp to date
        pub_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

        # Analyze sentiment
        sentiment = analyzer.analyze_sentiment(headline)
        compound_score = sentiment["compound"]

        print(f"- {pub_date} | {headline}")
        print(f"  Sentiment Score (compound): {compound_score:.3f}")
        print(f"  {url}\n")


if __name__ == "__main__":
    main()

