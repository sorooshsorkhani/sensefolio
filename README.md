# 📈 Sensefolio

**Sensefolio** is a personal project designed to analyze stock market news and trends, aiming to provide data-driven insights into the short-term behavior of a company's stock.

> 🛠️ This project is under active development and not yet production-ready.

## 🎯 Project Overview

Sensefolio combines real-time financial news with sentiment analysis and historical stock data to identify patterns that may influence stock performance. The goal is to build a system that provides a probability-based indication of whether a stock’s value may experience upward or downward momentum over a selected time frame.

It currently uses the VADER sentiment model to analyze news headlines and assess market sentiment.

## 💡 How It Helps

In today’s fast-moving markets, news plays a critical role in shaping investor sentiment. Sensefolio helps users by:

- Aggregating and organizing company-specific financial news from trusted sources
- Extracting sentiment from news articles using natural language processing (currently via VADER)
- Preparing the foundation for analyzing correlations between sentiment trends and stock price movements
- Laying the groundwork for building predictive models to assist in decision making

Whether you're an investor, a data enthusiast, or simply curious, Sensefolio aims to be a useful tool for exploring the relationship between media sentiment and stock trends.

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- A free [Finnhub API key](https://finnhub.io)

### 📦 Setup Instructions

```
# 1. Clone the repository
git clone https://github.com/your-username/sensefolio.git
cd sensefolio

# 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Copy the example file and insert your actual API key
cp .env.example .env
# Then edit .env and replace the placeholder with your API key

# 5. Run the CLI test
python -m app.backend.main
```

> The CLI will prompt for a stock symbol, fetch the latest news, and analyze the sentiment of each headline using VADER.

## 🛣️ Roadmap

- [x] Fetch latest financial news from Finnhub API
- [x] Perform sentiment analysis on news headlines using VADER
- [ ] Integrate historical stock price data *(coming soon)*
- [ ] Analyze correlations between sentiment and price movement *(planned)*
- [ ] Generate short-term movement probabilities *(planned)*
- [ ] Expose functionality via a REST API *(planned)*
- [ ] Build a frontend interface for user interaction *(planned)*
- [ ] Deploy the complete application *(planned)*

## 👤 About the Author

I'm [@sorooshsorkhani](https://github.com/sorooshsorkhani), a data scientist who enjoys using data to build meaningful, useful things.

I'm learning as I go, and this project is very much a work in progress — thanks for checking it out!

## 📢 Disclaimer

This is a personal learning project and **not intended as financial advice**. Always conduct your own research before making investment decisions.
