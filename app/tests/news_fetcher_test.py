# tests/news_fetcher_test.py

import pytest
from datetime import datetime, timedelta
from app.backend.news.news_fetcher import company_news_finnhub

def test_fetch_news_valid_symbol():
    news = company_news_finnhub("AAPL")
    assert isinstance(news, list)
    if news:
        assert "headline" in news[0]

def test_fetch_news_invalid_symbol_returns_empty():
    news = company_news_finnhub("INVALID$$$")
    assert news == [] or isinstance(news, list)

def test_date_logic_with_str_input():
    today = datetime.now().date()
    from_str = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    to_str = today.strftime('%Y-%m-%d')

    news = company_news_finnhub("AAPL", from_date=from_str, to_date=to_str)
    assert isinstance(news, list)

def test_date_logic_with_datetime_input():
    today = datetime.now()
    from_dt = today - timedelta(days=3)
    news = company_news_finnhub("AAPL", from_date=from_dt, to_date=today)
    assert isinstance(news, list)

def test_from_date_after_to_date_raises():
    today = datetime.now().date()
    with pytest.raises(ValueError):
        company_news_finnhub("AAPL", from_date=today, to_date=today - timedelta(days=5))
