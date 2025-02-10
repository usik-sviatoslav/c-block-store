#!/bin/bash

# Color codes
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
NO_COLOR="\033[0m"

# Database migration
echo -e "${GREEN}Running migrations...${NO_COLOR}"
python manage.py migrate

# Collecting static files
echo -e "\n${GREEN}Collecting static files...${NO_COLOR}"
python manage.py collectstatic --no-input

# Start server
if [[ "$ENV_STATE" == "production" || "$ENV_STATE" == "staging" ]]; then
  echo -e "\n${GREEN}Starting servers in $ENV_STATE mode...${NO_COLOR}"
  uvicorn core.fastapi.asgi:app --host 0.0.0.0 --port 8000 --workers 4 --use-colors &
  uvicorn core.django.asgi:app --host 0.0.0.0 --port 8001 --workers 1 --use-colors
else
  echo -e "\n${YELLOW}Starting servers in development mode...${NO_COLOR}"
  uvicorn core.fastapi.asgi:app --host 0.0.0.0 --port 8000 --reload --use-colors &
  uvicorn core.django.asgi:app --host 0.0.0.0 --port 8001 --reload --use-colors
fi
