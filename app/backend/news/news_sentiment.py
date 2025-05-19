# news_sentiment.py
# Module to fetch news, analyze sentiment, display results, and visualize sentiment trends.

import pandas as pd
import matplotlib.pyplot as plt
from app.backend.news.news_fetcher import fetch_company_news
from app.backend.sentiment.sentiment_analyzer import SentimentAnalyzer


def analyze_news_sentiment(symbol: str, verbose: bool = True) -> pd.DataFrame:
    """
    Fetches news for the given symbol and performs sentiment analysis on summaries.

    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL").
        verbose (bool): If True, print progress information.

    Returns:
        pd.DataFrame: DataFrame containing news with sentiment scores.
    """
    news_df = fetch_company_news(symbol, verbose=verbose)
    if news_df.empty:
        if verbose:
            print("⚠️  No news fetched to analyze.")
        return news_df

    analyzer = SentimentAnalyzer()

    def get_sentiment(text: str) -> float:
        if not text:
            return 0.0
        return analyzer.analyze_sentiment(text).get("compound", 0.0)

    news_df['summary_score'] = news_df['summary'].apply(get_sentiment)

    if verbose:
        print(f"[INFO] Analyzed sentiment for {len(news_df)} news articles.")

    return news_df


def show_news_sentiment(news_df: pd.DataFrame) -> None:
    """
    Displays the news sentiment in a nicely formatted table.
    """
    if news_df.empty:
        print("⚠️  No news available to display.")
        return

    def truncate_text(text: str, length: int = 100) -> str:
        return text[:length] + '...' if len(text) > length else text

    news_df['short_summary'] = news_df['summary'].apply(lambda x: truncate_text(str(x)))
    news_df = news_df.sort_values(by='datetime', ascending=False)

    display_df = news_df[['datetime', 'headline', 'short_summary', 'summary_score']]
    print("\n📰 News Sentiment Analysis (Latest to Oldest):")
    print(display_df.to_string(index=False))


def summarize_sentiment_scores(news_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and prints the average sentiment scores grouped by date.
    Returns a DataFrame for further use.
    """
    if news_df.empty:
        print("⚠️  No sentiment data to summarize.")
        return pd.DataFrame()

    news_df['date'] = news_df['datetime'].dt.date
    grouped = news_df.groupby('date').agg({'summary_score': 'mean'}).reset_index()

    print("\n📊 Average Sentiment Scores by Date:")
    print(grouped.to_string(index=False))
    return grouped


def visualize_news_sentiment(news_df: pd.DataFrame) -> None:
    """
    Visualizes the average sentiment scores for headlines and summaries grouped by date.
    """
    grouped = summarize_sentiment_scores(news_df)
    if grouped.empty:
        print("⚠️  No data available for visualization.")
        return

    plt.figure(figsize=(10, 6))
    width = 0.4

    # Fix date format and include missing dates
    grouped['date'] = pd.to_datetime(grouped['date']).dt.strftime('%Y-%m-%d')

    # Create a full date range and merge to include missing dates
    full_date_range = pd.date_range(start=grouped['date'].min(), end=grouped['date'].max())
    full_dates = pd.DataFrame(full_date_range, columns=['date'])
    full_dates['date'] = full_dates['date'].dt.strftime('%Y-%m-%d')
    grouped = pd.merge(full_dates, grouped, on='date', how='left').fillna(0)

    plt.bar(
        grouped['date'],
        grouped['summary_score'],
        width=width,
        color='deepskyblue',
        label='Summary Score',
        align='edge'
    )

    plt.title("Average Sentiment Scores by Date")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()



def main():
    print("📰 News Sentiment Analyzer")
    symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
    sentiment_df = analyze_news_sentiment(symbol)
    show_news_sentiment(sentiment_df)
    visualize_news_sentiment(sentiment_df)


if __name__ == "__main__":
    main()
