#!/bin/bash

await_service() {
  while ! /src/scripts/healthcheck.py --service "$1" --timeout "$2" --retries "$3"; do
    exit 1
  done
}

await_postgres() {
  await_service postgres 20 5
}

await_redis() {
  await_service redis 20 5
}

await_celery_db_table() {
  await_service celery_db_table 20 5
}
