# sentiment_analyzer_cli_test.py

from app.backend.sentiment.sentiment_analyzer import SentimentAnalyzer

def main():
    print("🧠 Sentiment Analyzer CLI Test (VADER)")

    analyzer = SentimentAnalyzer()

    while True:
        text = input("\nEnter a sentence (or 'q' to quit): ").strip()
        if text.lower() == "q":
            break

        scores = analyzer.analyze_sentiment(text)
        print(f"Sentiment Scores: {scores}")

if __name__ == "__main__":
    main()
