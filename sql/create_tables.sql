-- Create airflow database and user
CREATE USER airflow WITH PASSWORD 'airflow123';
CREATE DATABASE airflow OWNER airflow;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

-- Create sentiment database
CREATE DATABASE sentiment OWNER postgres;

-- Connect to sentiment database and create tables
\c sentiment;

-- Raw social media posts table
CREATE TABLE IF NOT EXISTS raw_posts (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(100) UNIQUE NOT NULL,
    platform VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100),
    created_at TIMESTAMP,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    extracted_at TIMESTAMP DEFAULT NOW()
);

-- Processed sentiment data table
CREATE TABLE IF NOT EXISTS sentiment_analysis (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(100) NOT NULL,
    cleaned_content TEXT,
    sentiment_score NUMERIC(5,2),
    sentiment_label VARCHAR(20),
    confidence_score NUMERIC(5,2),
    word_count INTEGER,
    processed_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (post_id) REFERENCES raw_posts(post_id) ON DELETE CASCADE
);

-- ETL monitoring table
CREATE TABLE IF NOT EXISTS etl_logs (
    id SERIAL PRIMARY KEY,
    dag_id VARCHAR(100),
    task_id VARCHAR(100),
    execution_date TIMESTAMP,
    status VARCHAR(20),
    records_processed INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_raw_posts_created_at ON raw_posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_raw_posts_platform ON raw_posts(platform);
CREATE INDEX IF NOT EXISTS idx_sentiment_label ON sentiment_analysis(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_sentiment_processed_at ON sentiment_analysis(processed_at DESC);

-- Insert sample data for testing
INSERT INTO raw_posts (post_id, platform, content, author, created_at, likes, shares) 
VALUES 
    ('sample_001', 'twitter', 'I love this new product! Amazing quality and great service.', 'user123', NOW() - INTERVAL '1 day', 45, 12),
    ('sample_002', 'facebook', 'Terrible experience with customer support. Very disappointed.', 'user456', NOW() - INTERVAL '2 hours', 3, 1),
    ('sample_003', 'instagram', 'This is okay, nothing special but not bad either.', 'user789', NOW() - INTERVAL '30 minutes', 8, 2)
ON CONFLICT (post_id) DO NOTHING;

-- Grant permissions for airflow user to access sentiment database
GRANT CONNECT ON DATABASE sentiment TO airflow;
\c sentiment;
GRANT USAGE ON SCHEMA public TO airflow;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO airflow;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO airflow;
