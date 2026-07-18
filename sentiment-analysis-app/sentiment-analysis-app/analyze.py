"""
analyze.py
-----------
Core sentiment analysis logic.

Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) from NLTK.
Why VADER for this project?
- Rule-based, no training data required (great for a beginner-explainable demo)
- Tuned specifically for short, informal text like reviews and social media
- Handles negation ("not good") and intensity ("VERY good!!!") out of the box
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


def _ensure_vader_lexicon() -> None:
    """Download VADER's lexicon once, only if it isn't already on disk."""
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


_ensure_vader_lexicon()
_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a single piece of text.

    Args:
        text: Raw input string (e.g. a customer review or feedback message).

    Returns:
        {
            "label":  "Positive" | "Negative" | "Neutral",
            "score":  compound score, range -1.0 (most negative) to +1.0 (most positive),
            "scores": full breakdown -> {"neg": .., "neu": .., "pos": .., "compound": ..}
        }
    """
    if not text or not text.strip():
        return {"label": "Neutral", "score": 0.0, "scores": {}}

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]

    # Standard VADER thresholds (used widely in industry/academic benchmarks)
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {"label": label, "score": compound, "scores": scores}


if __name__ == "__main__":
    # Quick manual sanity check - run with: python analyze.py
    samples = [
        "This product is absolutely amazing, I love it!",
        "Terrible service, I want a refund immediately.",
        "The package arrived on Tuesday.",
        "Not bad, but I expected more for the price.",
    ]
    for s in samples:
        result = analyze_sentiment(s)
        print(f"{s!r:55} -> {result['label']:9} (score: {result['score']:+.2f})")
