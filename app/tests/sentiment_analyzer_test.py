# sentiment_analyzer_test.py

import pytest
from app.backend.sentiment.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def analyzer():
    return SentimentAnalyzer()

def test_positive_sentiment(analyzer):
    text = "This product is amazing and I love it!"
    result = analyzer.analyze_sentiment(text)
    assert result["compound"] > 0

def test_negative_sentiment(analyzer):
    text = "This is the worst service I’ve ever experienced."
    result = analyzer.analyze_sentiment(text)
    assert result["compound"] < 0

def test_neutral_sentiment(analyzer):
    text = "The meeting was scheduled at 3 PM."
    result = analyzer.analyze_sentiment(text)
    assert abs(result["compound"]) < 0.1

def test_score_keys_exist(analyzer):
    text = "Hello world"
    result = analyzer.analyze_sentiment(text)
    for key in ["compound", "pos", "neu", "neg"]:
        assert key in result

def test_invalid_model_raises():
    with pytest.raises(NotImplementedError):
        SentimentAnalyzer(model="unknown_model")
