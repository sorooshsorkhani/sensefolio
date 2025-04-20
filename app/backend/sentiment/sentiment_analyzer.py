# sentiment_analyzer.py
# Module for sentiment analysis using pluggable models (currently VADER)

from typing import Literal, Dict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure VADER lexicon is downloaded (do once)
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


class SentimentAnalyzer:
    """
    A modular sentiment analyzer that supports different models.

    Supported models:
    - vader (default): rule-based sentiment analysis optimized for short text
    """

    def __init__(self, model: Literal["vader"] = "vader"):
        """
        Initializes the sentiment analyzer with the specified model.

        Args:
            model (str): The name of the sentiment model to use.
                         Currently supports "vader".
        """
        self.model_name = model

        if model == "vader":
            self.analyzer = SentimentIntensityAnalyzer()
        else:
            raise NotImplementedError(f"Model '{model}' is not implemented yet.")

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyzes the sentiment of a given text.

        Args:
            text (str): The input text to analyze (e.g., a news headline).

        Returns:
            dict: A dictionary with sentiment scores.
                  Example (for VADER):
                  {
                      "compound": 0.6249,
                      "pos": 0.321,
                      "neu": 0.656,
                      "neg": 0.023
                  }
        """
        if self.model_name == "vader":
            return self.analyzer.polarity_scores(text)

        raise NotImplementedError(f"Model '{self.model_name}' is not implemented yet.")
