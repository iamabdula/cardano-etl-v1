# Cardano ETL Pipeline

This repository implements an ETL pipeline for Cardano’s Sustainable Investment team. The project demonstrates two implementation stages:

- **Branch: Draft 1:** A simple virtual environment (venv) setup without Docker or Airflow.
- **Branch: Draft 2:** A production-ready setup with Docker and Apache Airflow for orchestration, along with robust error handling, logging, and unit tests.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Draft 1: Virtual Environment Setup](#draft-1-virtual-environment-setup)
- [Draft 2: Dockerization & Airflow Setup](#draft-2-dockerization--airflow-setup)
  - [Airflow Configuration & Environment Variables](#airflow-configuration--environment-variables)
  - [Docker Compose & Commands](#docker-compose--commands)
  - [Accessing the Airflow UI](#accessing-the-airflow-ui)
  - [Triggering and Testing the Pipeline](#triggering-and-testing-the-pipeline)
- [Running Unit Tests](#running-unit-tests)
- [Output Files](#output-files)
- [Additional Insights](#additional-insights)
- [Branching Strategy](#branching-strategy)

---

## Project Structure

cardano_etl/
├── dags/                 # Airflow DAGs (Draft 2)
│   └── etl_dag.py
├── data/                 # Input data files (CSV, JSON, XML) and output files
├── src/                  # ETL pipeline source code
│   ├── ingestion.py
│   ├── transformation.py
│   ├── storage.py
│   └── main.py
├── tests/                # Unit tests for each module
│   ├── test_ingestion.py
│   ├── test_transformation.py
│   └── test_storage.py
├── airflow_data/         # Persistent volume for Airflow metadata (Draft 2)
├── logs/                 # Logs for Airflow (Draft 2)
├── Dockerfile            # Dockerfile for building the ETL image
├── docker-compose.yml    # Docker Compose configuration for Airflow and related services
├── requirements.txt      # Production dependencies
└── requirements-test.txt  # Development/testing dependencies (e.g., pytest)


# Draft 1: Virtual Environment Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
PYTHONPATH=. pytest tests/

# Draft 2: Dockerization & Airflow Setup
Fernet Key:

# Airflow uses a Fernet key to encrypt sensitive data. Generate one by running:
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

  Copy the generated key and set it in your docker-compose.yml under the environment section for both the airflow-webserver and airflow-scheduler services:
    environment:
  - AIRFLOW__CORE__FERNET_KEY=YOUR_GENERATED_FERNET_KEY

# Docker Compose & Commands
  docker build -t cardano_etl .
  docker-compose up -d
  If you encounter database initialization errors, run:
      docker-compose run --rm airflow-webserver airflow db init
      docker-compose down
      docker-compose up -d


# Create an Admin User (if not already created) by running:
docker-compose run --rm airflow-webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com


# DAG Setup:
Your DAG (dags/etl_dag.py) is automatically loaded by Airflow. Since schedule_interval is set to None, manually trigger the DAG via the Airflow UI.

# BashOperator Volume Mapping:

  import os
  local_path = os.getcwd()  # Dynamically obtains your local project directory
  run_etl = BashOperator(
      task_id='run_etl',
      bash_command=f'docker run --mount type=bind,source={local_path}/output,target=/app/data cardano_etl',
      dag=dag,
  )


# Output Files:
The ETL pipeline writes output files (e.g., CSV) to the output directory. Check this folder on your host after a successful run.


# Running Unit Tests
pip install -r requirements-dev.txt
PYTHONPATH=. pytest tests/


## Additional Insights
  # Error Handling & Logging:
    Each module (ingestion, transformation, storage) implements structured error handling using Python’s logging module. Detailed logs help diagnose issues in production.

  # Stability & Resilience:
    The pipeline is designed for idempotency and robust error handling, with Airflow configured to retry tasks and enforce SLAs.

  # Continuous Integration/Delivery:
    Integrate your tests into a CI/CD pipeline (using GitHub Actions, GitLab CI, etc.) to automatically run tests and build Docker images upon commits.

  # Local File Sharing:
    Ensure your local project directory is shared with Docker Desktop (via Preferences → Resources → File Sharing) if running on macOS or Windows.


## Branching Strategy
  # Draft 1:
    Contains the simple venv setup without Docker/Airflow.
    Used for initial development and testing.
  # Draft 2:
    Contains Docker and Airflow integration.
    Includes detailed instructions for setting up Docker, initializing Airflow, logging into the Airflow UI, triggering the pipeline, and verifying output files.


## Summary
  # Draft 1 (Venv Setup):
  Run the ETL pipeline with python src/main.py.
  Use pytest for unit tests.
  
  # Draft 2 (Docker & Airflow):
  Build the Docker image with docker build -t cardano_etl ..
  Bring up the environment with docker-compose up -d.
  Initialize the Airflow database if needed.
  Access the Airflow UI at http://localhost:8080, log in, and trigger the pipeline.
  Verify output files in the designated output folder.
