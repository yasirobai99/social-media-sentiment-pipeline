import os, psycopg2

def main():
    conn = psycopg2.connect(
        host="postgres",
        database="sentiment",
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PWD", "postgres123"),
    )
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM raw_posts;")
        count = cur.fetchone()[0]
        print(f"raw_posts table initialized. Row count: {count}")

if __name__ == "__main__":
    main()
