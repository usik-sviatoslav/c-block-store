# Builder stage
FROM python:3.11-slim AS builder

ARG USERNAME=code
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /src

# Create user and group
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash

# Installing system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    pip install --no-cache-dir --upgrade pip setuptools poetry && \
    rm -rf /var/lib/apt/lists/*

# Copying only dependency files
COPY pyproject.toml /src/

ARG ENV_STATE
ARG FLAG

# Setting the flag depending on ENV_STATE
RUN FLAG=$( [ "$ENV_STATE" = "staging" ] || [ "$ENV_STATE" = "production" ] && echo "--no-dev" || echo "")

# Installing Poetry dependencies
RUN poetry install --no-root $FLAG && \
    poetry cache clear . --all --no-interaction


# Base stage
FROM python:3.11-slim AS base

ARG USERNAME=code

WORKDIR /src

# Installing system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends supervisor && \
    rm -rf /var/lib/apt/lists/*

# Copy system dependencies
COPY --from=builder /usr/local /usr/local
COPY --from=builder /etc/group /etc/group
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /home/$USERNAME /home/$USERNAME

# Copying project source code
COPY ./src /src/
COPY ./setup.conf /etc/supervisor/conf.d/

# Creating log directories and grant permissions
RUN mkdir -p /var/log/backend/access && \
    mkdir -p /var/log/backend/celery && \
    mkdir -p /var/log/backend/django && \
    mkdir -p /var/log/backend/fastapi && \
    chown -R $USERNAME:$USERNAME /var/log/backend

# Select internal user
USER $USERNAME
