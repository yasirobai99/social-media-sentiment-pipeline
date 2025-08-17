import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from src.data_transformation.text_preprocessor import clean_text
from src.data_transformation.sentiment_analyzer import analyze_sentiment
from datetime import datetime

def process_and_store_sentiments(batch_size=400):
    print("[DEBUG] START OF FUNCTION - process_and_store_sentiments")
    engine = create_engine("postgresql://postgres:postgres123@postgres:5432/sentiment")
    total_processed = 0
    batch_num = 0

    while True:
        query = f"""
            SELECT post_id, content
            FROM raw_posts rp
            WHERE NOT EXISTS (
                SELECT 1 FROM sentiment_analysis sa WHERE sa.post_id = rp.post_id
            )
            LIMIT {batch_size};
        """
        t1 = datetime.now()
        df = pd.read_sql(query, engine)
        t2 = datetime.now()
        print(f"[TIMER] Batch {batch_num+1} SQL fetch: {(t2-t1).total_seconds()}s, df.shape={df.shape}")

        if df.empty:
            print("[DEBUG] No new posts found. DONE.")
            break

        results = []
        t3 = datetime.now()
        for _, row in df.iterrows():
            cleaned = clean_text(row['content'])
            sentiment = analyze_sentiment(cleaned)
            results.append((
                row['post_id'],
                cleaned,
                sentiment['sentiment_score'],
                sentiment['sentiment_label'],
                sentiment['confidence_score'],
                sentiment['word_count'],
            ))
        t4 = datetime.now()
        print(f"[TIMER] Batch {batch_num+1} Sentiment: {(t4-t3).total_seconds()}s for {len(results)} rows")

        if results:
            try:
                t5 = datetime.now()
                conn = psycopg2.connect(
                    host="postgres",
                    database="sentiment",
                    user=os.getenv("POSTGRES_USER", "postgres"),
                    password=os.getenv("POSTGRES_PASSWORD", "postgres123"),
                )
                insert_query = """
                    INSERT INTO sentiment_analysis
                    (post_id, cleaned_content, sentiment_score, sentiment_label, confidence_score, word_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (post_id) DO NOTHING;
                """
                cur = conn.cursor()
                cur.executemany(insert_query, results)
                conn.commit()
                cur.close()
                conn.close()
                t6 = datetime.now()
                print(f"[TIMER] Batch {batch_num+1} Insert: {(t6-t5).total_seconds()}s")
                print(f"[DEBUG] Inserted {len(results)} rows in batch {batch_num+1}.")
                total_processed += len(results)
                batch_num += 1
                print(f"[PROGRESS] Completed batch #{batch_num}, total processed: {total_processed}")
            except Exception as e:
                print("[ERROR] Exception during INSERT:", str(e))
                raise
        else:
            break

    print(f"[DEBUG] Finished. Total processed: {total_processed}")
    return total_processed
