# dags/etl_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'cardano_etl',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cardano_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Cardano transactions data',
    # schedule_interval=timedelta(days=1),
    schedule_interval=None,  # No automatic scheduling

)


# Task to run the ETL process using the Docker container we built
run_etl = BashOperator(
    task_id='run_etl',
    bash_command='docker run -v /Users/user/Documents/appl/cardano_etl/output:/app/data cardano_etl',
    dag=dag,
)

run_etl