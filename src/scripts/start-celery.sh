#!/bin/bash

source /src/scripts/healthcheck.sh
source /src/scripts/logging.sh


start_celery() {
  if [[ "$CELERY_TYPE" == "worker" ]]; then
    log_message INFO "Starting Celery Worker..."
    celery -A core.config worker --loglevel=info --autoscale=2,1

  elif [[ "$CELERY_TYPE" == "beat" ]]; then
    log_message INFO "Starting Celery Beat..."
    celery -A core.config beat --loglevel=info
  else
    log_message ERROR "Unknown Celery type: $CELERY_TYPE"
    exit 1
  fi
}

await_redis
await_postgres
await_celery_db_table

start_celery
