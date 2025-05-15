# news_fetcher.py
# Module responsible for fetching financial news from Finnhub API.

import requests
from datetime import datetime, timedelta
from typing import Union
from app.backend.config import FINNHUB_API_KEY

# Base URL for Finnhub API
BASE_URL = "https://finnhub.io/api/v1"

def company_news_finnhub(
    symbol: str,
    from_date: Union[str, datetime, None] = None,
    to_date: Union[str, datetime, None] = None,
    verbose: bool = False
) -> list:
    """
    Fetches company-related news articles from the Finnhub API.

    Args:
        symbol (str): Stock ticker symbol (e.g., "AAPL").
        from_date (str | datetime | None): Start date in 'YYYY-MM-DD' format or datetime object.
                                           If None, defaults based on to_date or today.
        to_date (str | datetime | None): End date in 'YYYY-MM-DD' format or datetime object.
                                         If None, defaults to today or 7 days after from_date.
        verbose (bool): If True, prints progress and error messages.

    Returns:
        list: List of dictionaries containing news articles.

    Notes:
        - If from_date is after to_date, function raises a ValueError.
        - Accepts both string and datetime inputs for flexibility.
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
        if response.status_code == 200:
            if verbose:
                print(f"[INFO] Retrieved news for {symbol} from {from_str} to {to_str}")
            return response.json()
        else:
            if verbose:
                print(f"[ERROR {response.status_code}] {response.text}")
            return []
    except requests.RequestException as e:
        if verbose:
            print(f"[EXCEPTION] Failed to fetch news: {e}")
        return []


def main():
    print("📰 Sensefolio News Fetcher")
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
