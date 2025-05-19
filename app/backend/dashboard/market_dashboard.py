# market_dashboard.py
# Dashboard combining stock price trends and news sentiment in one plot.

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from app.backend.price.stock_data import get_data
from app.backend.news.news_sentiment import analyze_news_sentiment


def aggregate_sentiment_to_trading_dates(news_df: pd.DataFrame, trading_dates: list) -> pd.DataFrame:
    """
    Roll forward each news item to the next trading date, then average by trading_date.
    """
    temp = news_df.copy()
    temp['news_date'] = temp['datetime'].dt.date

    sorted_trading = sorted(trading_dates)
    def map_date(nd):
        for td in sorted_trading:
            if td >= nd:
                return td
        return None

    temp['trade_date'] = temp['news_date'].apply(map_date)
    temp = temp.dropna(subset=['trade_date'])

    series = temp.groupby('trade_date')['summary_score'].mean()
    series = series.reindex(sorted_trading, fill_value=0)

    grouped = series.reset_index()
    grouped.columns = ['trade_date', 'summary_score']
    return grouped


def plot_dashboard(symbol: str):
    # 1) Fetch price data
    data, current_price = get_data(symbol)
    if data is None:
        print(f"Failed to fetch price data for {symbol}.")
        return

    # Historical dates & values
    hist_dates = [d.date() for d in data.index]
    hist_vals = list(data['Close'])

    # Check if we need to add today's price
    today = datetime.now().date()
    append_current = (current_price is not None and today not in hist_dates)

    trading_dates = hist_dates.copy()
    if append_current:
        trading_dates.append(today)

    # 2) Fetch & aggregate sentiment
    news_df = analyze_news_sentiment(symbol, verbose=False)
    if not news_df.empty:
        sentiment_df = aggregate_sentiment_to_trading_dates(news_df, trading_dates)
    else:
        sentiment_df = pd.DataFrame({
            'trade_date': trading_dates,
            'summary_score': [0]*len(trading_dates)
        })

    # String-format labels
    price_labels = [d.strftime('%Y-%m-%d') for d in hist_dates]
    all_labels = [d.strftime('%Y-%m-%d') for d in trading_dates]

    # 3) Build one figure with two stacked axes (single frame)
    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(5, 1)
    ax_price = fig.add_subplot(gs[0:4, 0])
    ax_sent = fig.add_subplot(gs[4, 0], sharex=ax_price)

    # Plot price
    ax_price.plot(
        price_labels,
        hist_vals,
        color='blue', marker='o', linestyle='-',
        label='Close Price'
    )
    # Plot connector to current
    if append_current:
        ax_price.plot(
            [price_labels[-1], all_labels[-1]],
            [hist_vals[-1], current_price],
            color=('green' if current_price > hist_vals[-1] else 'red'),
            marker='o', linestyle='-',
            label='Current Price'
        )
    ax_price.set_ylabel('Price')
    ax_price.legend(loc='upper left')
    ax_price.grid(True)

    # Prepare bar colors: positive=deepskyblue, negative=orangered
    colors = ['deepskyblue' if val >= 0 else 'orangered' for val in sentiment_df['summary_score']]

    # Plot sentiment bars in bottom band
    ax_sent.bar(
        all_labels,
        sentiment_df['summary_score'],
        width=0.6,
        color=colors,
        align='edge',
        label='Avg. Sentiment'
    )
    # Draw horizontal zero line
    ax_sent.axhline(0, color='gray', linewidth=1)

    ax_sent.set_xlabel('Date')
    ax_sent.set_ylabel('Sentiment')
    ax_sent.legend(loc='upper right')
    ax_sent.grid(False)

    # Hide x tick labels on price axis
    plt.setp(ax_price.get_xticklabels(), visible=False)
    plt.subplots_adjust(hspace=0)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    sym = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
    plot_dashboard(sym)


if __name__ == '__main__':
    main()
