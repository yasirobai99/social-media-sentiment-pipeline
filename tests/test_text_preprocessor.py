from src.data_transformation.text_preprocessor import clean_text

def test_clean_text_basic():
    txt = "Hello 🙂 visit https://x.com @user #tag"
    out = clean_text(txt)
    assert isinstance(out, str)
    assert "http" not in out and "@" not in out and "#" not in out
    assert len(out) > 0
