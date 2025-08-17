# Runbook

Start
- docker-compose --env-file .env up -d

Stop
- docker-compose down

Restart
- docker-compose restart

Trigger DAG
- docker exec -it social-media-sentiment-pipeline-airflow-webserver-1 bash -lc "airflow dags trigger kaggle_social_media_extract"

Check counts
- docker exec -it social-media-sentiment-pipeline-postgres-1 psql -U postgres -d sentiment -c "SELECT COUNT(*) FROM sentiment_analysis;"

Backup now
- .\scripts\backup_now.ps1

Common issues
- Auth mismatch: ensure .env values match Airflow connection string.
- Inserts failing: ensure UNIQUE(post_id) on sentiment_analysis.
- Power BI connection: server=localhost, database=sentiment, ensure md5 in pg_hba.conf for 127.0.0.1/32 if needed.
