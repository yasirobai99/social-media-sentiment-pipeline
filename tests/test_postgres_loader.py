from src.data_loading.postgres_loader import build_insert_query

def test_build_insert_query_on_conflict():
    cols = ["post_id","cleaned_content","sentiment_score"]
    q, params = build_insert_query("sentiment_analysis", cols, on_conflict="post_id")
    assert "INSERT INTO sentiment_analysis" in q
    assert "ON CONFLICT (post_id) DO NOTHING" in q
    assert len(params) == len(cols)
