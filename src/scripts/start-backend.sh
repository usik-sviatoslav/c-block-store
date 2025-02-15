#!/bin/bash

source /src/scripts/healthcheck.sh
source /src/scripts/logging.sh


run_migrations() {
  log_message INFO "Running migrations..."
  python manage.py migrate
}

collect_static() {
  log_message INFO "Collecting static files..."
  python manage.py collectstatic --no-input
}

start_backend() {
  if [[ "$ENV_STATE" == "production" || "$ENV_STATE" == "staging" ]]; then
    log_message INFO "Starting servers in ${GREEN}$ENV_STATE mode${NO_COLOR}..."
  else
    log_message WARNING "Starting servers in ${YELLOW}development mode${NO_COLOR}..."
  fi
  supervisord -n -c /etc/supervisor/conf.d/setup.conf
}

await_postgres
await_redis

run_migrations
collect_static
start_backend
