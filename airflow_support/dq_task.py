import os
import psycopg2

def run_sql_file(path: str):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "sentiment"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres123"),
    )
    try:
        with conn, conn.cursor() as cur, open(path, "r", encoding="utf-8") as f:
            cur.execute(f.read())
            row = cur.fetchone()
            ok = row[0] if row else 0
            if ok != 1:
                raise Exception(f"Data quality check failed for {path}")
    finally:
        conn.close()
