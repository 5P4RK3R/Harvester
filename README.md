# Harvester

## Set Root before each command
`export AIRFLOW_HOME=$(pwd)/`
## Initialize the DB
`airflow db init`

## Create user's credentials
`airflow users create --username admin --password admin --firstname Mahendra --lastname Gurunathan --role Admin --email mahendragurunathan@gmail.com`
## Start the airflow webserver
`airflow webserver --port 8080`

## Start the airflow Scheduler
`airflow schedular`

## Trigger a DAG
`airflow dags trigger harvester`
