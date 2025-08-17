from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    label = 'positive' if score > 0.1 else 'negative' if score < -0.1 else 'neutral'
    return {
        'sentiment_score': round(score, 3),
        'sentiment_label': label,
        'confidence_score': round(abs(score), 3),
        'word_count': len(text.split())
    }