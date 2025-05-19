# news_fetcher.py
# news fetcher with structured output and data stored in a DataFrame.

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Union
from app.backend.config import FINNHUB_API_KEY

# Base URL for Finnhub API
BASE_URL = "https://finnhub.io/api/v1"


def fetch_company_news(
        symbol: str,
        from_date: Union[str, datetime, None] = None,
        to_date: Union[str, datetime, None] = None,
        verbose: bool = False
        ) -> pd.DataFrame:
    """
    Fetches company-related news articles from the Finnhub API and returns a DataFrame.
    """
    today = datetime.now().date()

    # Convert strings to datetime.date if needed
    if isinstance(from_date, str):
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    if isinstance(to_date, str):
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

    # Determine default values based on what's provided
    if from_date is None and to_date is None:
        to_date = today
        from_date = to_date - timedelta(days=7)
    elif from_date is None:
        from_date = to_date - timedelta(days=7)
    elif to_date is None:
        to_date = today

    # Final check: from_date should not be after to_date
    if from_date > to_date:
        raise ValueError("from_date cannot be after to_date.")

    # Format dates to string for API request
    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    # Construct API URL and parameters
    url = f"{BASE_URL}/company-news"
    params = {
        "symbol": symbol.upper(),
        "from": from_str,
        "to": to_str,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        if verbose:
            print(f"[INFO] Retrieved news for {symbol} from {from_str} to {to_str}")
        news = response.json()
        # Convert to DataFrame and sort by datetime
        df = pd.DataFrame(news)
        if not df.empty:
            df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
            df.sort_values(by='datetime', ascending=False, inplace=True)
        return df
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch news: {e}")
        return pd.DataFrame()


def display_news(
        df: pd.DataFrame,
        symbol: str
        ) -> None:
    """
    Displays the news headlines, grouped by date and sorted by time.
    """
    if df.empty:
        print("⚠️  No news found.")
        return

    print(f"\n📢 All news headlines for {symbol}, grouped by date:")
    # Grouping and displaying news
    for date, group in df.groupby(df['datetime'].dt.date, sort=False):
        print(f"\n📅 {date}")
        for _, article in group.iterrows():
            time_str = article['datetime'].strftime('%H:%M')
            headline = article.get("headline", "No headline available")
            url = article.get("url", "No URL available")
            summary = article.get("summary", "No summary available")
            print(f"  🕒 {time_str} - {headline}")
            print(f"     {url}")
            if summary:
                print(f"     📝 {summary}")


def main():
    print("📰 Sensefolio News Fetcher")
    symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
    news_df = fetch_company_news(symbol, verbose=True)
    display_news(news_df, symbol)


if __name__ == "__main__":
    main()
