# Project Overview: Airflow ETL with Postgres & NASA API
This project builds an ETL pipeline with Apache Airflow, pulling data from NASA’s Astronomy Picture of the Day (APOD) API, transforming it, and storing it in a Postgres database. Everything runs in Docker for an isolated, reproducible setup.

## Key Components
Airflow (Orchestration)
Manages and schedules the ETL workflow with a DAG (Directed Acyclic Graph).

Ensures tasks run in the right order and are easy to monitor.

Postgres (Storage)
Stores the processed data in a table.

Runs in a Docker container with persistent storage via Docker volumes.

Accessed using Airflow’s PostgresHook and PostgresOperator.

NASA APOD API (Data Source)
Provides daily astronomy pictures with metadata (title, explanation, URL).

Airflow’s HttpOperator fetches the API data.

# Astro deploy

Finally, I created an AWS postgres database, and use the endpoint to connect with cloud DAG deployment on Astro