import re

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)
    text = text.lower().strip()
    return text