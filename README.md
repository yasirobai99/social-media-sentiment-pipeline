# Overview
Welcome to the Social Media Sentiment Pipeline! This README explains what’s inside the project and how to run Apache Airflow with PostgreSQL on a local machine using Docker.

# Project Contents
Your project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. The primary DAG orchestrates extracting raw posts, cleaning text, computing sentiment, and loading results into PostgreSQL.
- src: Application code used by the DAGs.
  - data_extraction: Scripts to fetch/load raw data into staging tables.
  - data_transformation: Utilities for text cleaning and sentiment scoring.
  - data_loading: Helpers to batch-insert data into PostgreSQL safely.
  - utils: Shared helpers (logging, config, small wrappers).
- sql: SQL assets used by the pipeline.
  - data_quality: Standalone SQL checks for row counts, score ranges, and duplicate IDs.
  - other DDL/utility SQL files as needed by the DAGs.
- airflow_support: Small helper modules invoked from tasks (for example, a function that runs an external SQL file and asserts pass/fail).
- scripts: Operational scripts for local use (for example, a PowerShell script to create timestamped PostgreSQL backups).
- config: Configuration folder mounted into containers (for example, local credentials paths). Keep secrets out of version control.
- powerbi: Placeholder for reports and visuals. Binary report files (.pbix) are intentionally ignored by Git.
- docs: Lightweight documentation such as a runbook and troubleshooting notes.
- tests and pytest.ini: Optional testing scaffolding for modules/DAG import checks. Useful for local validation and future CI.
- docker-compose.yml: Orchestration file that starts PostgreSQL, pgAdmin, Airflow Webserver, and Airflow Scheduler with the correct mounts and environment.

# Deploy Your Project Locally
- Start:  
  docker-compose --env-file .env up -d

- Components started:  
  Postgres (DB), pgAdmin (DB UI), Airflow Webserver (UI), Airflow Scheduler (tasks)

- Check:  
  docker ps

- Default ports:  
  Airflow 8080, Postgres 5432, pgAdmin 5050

- Access:  
  Airflow: http://localhost:8080 (admin/admin by default from .env)  
  Postgres: localhost:5432 (DB: sentiment, user/pass from .env)  
  pgAdmin: http://localhost:5050 (email/pass from .env; add server host=postgres)
