import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(dataset_name, **context):
    data_path = '/tmp/kaggle_data'
    os.makedirs(data_path, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset_name, path=data_path, unzip=True)
    print(f"[INFO] Downloaded and extracted {dataset_name} to {data_path}")

def load_to_postgres(**context):
    import pandas as pd
    import psycopg2

    data_path = '/tmp/kaggle_data'
    csv_file = os.path.join(data_path, 'training.1600000.processed.noemoticon.csv')
    df = pd.read_csv(csv_file, encoding='latin-1', header=None, names=['target', 'id', 'date', 'flag', 'user', 'content'])

    conn = psycopg2.connect(
        host="postgres",
        dbname="sentiment",
        user="postgres",
        password="postgres123"
    )
    cur = conn.cursor()
    for _, row in df.head(10000).iterrows():  # For demo, import just 10k rows
        cur.execute(
            "INSERT INTO raw_posts (post_id, platform, content, author, created_at, likes, shares) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (str(row['id']), 'twitter', row['content'], row['user'], row['date'], 0, 0)
        )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[INFO] Loaded posts into raw_posts table.")
