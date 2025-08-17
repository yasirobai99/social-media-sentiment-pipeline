from src.data_transformation.sentiment_analyzer import SentimentAnalyzer
sa = SentimentAnalyzer()

def test_vader_range_and_label():
    s, label, conf = sa.analyze_with_vader("I love this!")
    assert -1.0 <= s <= 1.0
    assert label in {"Positive","Negative","Neutral"}
    assert 0.0 <= conf <= 1.0
