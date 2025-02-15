#!/usr/bin/env python
import argparse
import logging.config
import os
import sys
import time
from functools import wraps
from typing import Any, Callable

import psycopg2
import redis
from psycopg2 import DatabaseError, OperationalError

sys.path.append(os.path.abspath("/src"))

logger = logging.getLogger("healthcheck")
logger.setLevel(logging.INFO)

dbname = os.getenv("POSTGRES_DB", "c-block-store")
host = os.getenv("POSTGRES_HOST", "postgres")
port = int(os.getenv("POSTGRES_PORT", "5432"))
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")


def retry_with_timeout(  # noqa: CFQ004
    service_name: str, timeout: int, retries: int
) -> Callable[[Callable[..., int]], Callable[..., int]]:
    """Decorator to retry the function with timeout and logging."""

    def decorator(func: Callable[..., int]) -> Callable[..., int]:  # noqa: CFQ004
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> int:
            start_time = time.time()

            messages = {
                "start": f"Check connection with {service_name}...",
                "ready": f"{service_name} is ready to accept a connection!",
                "max_retries": f"Max retries reached. {service_name} is still unavailable.\n",
                "timeout": f"Timeout reached ({timeout}s). {service_name} is still unavailable.\n",
            }

            logger.info(messages["start"])
            for attempt in range(1, retries + 1):
                try:
                    if func(*args, **kwargs) == 0:
                        logger.info(messages["ready"])
                        return 0
                    raise ConnectionError

                except (OperationalError, DatabaseError, ConnectionError, TimeoutError):
                    elapsed_time = time.time() - start_time

                    if elapsed_time >= timeout:
                        logger.error(messages["timeout"])
                        return 1

                    time.sleep(2)

            logger.error(messages["max_retries"])
            return 1

        return wrapper

    return decorator


def check_postgres(timeout: int, retries: int) -> int:
    """Check if PostgreSQL service is available."""

    @retry_with_timeout("PostgreSQL", timeout, retries)
    def _check() -> int:
        with psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=password):
            return 0

    return _check()


def check_db_table(timeout: int, retries: int) -> int:
    """Check if database table exists."""

    @retry_with_timeout("The table like `django_celery_%`", timeout, retries)
    def _check() -> int:
        with psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=password) as conn:
            query = "SELECT tablename FROM pg_tables WHERE tablename LIKE 'django_celery_%' LIMIT 1;"
            cur = conn.cursor()
            cur.execute(query)
            return 0 if cur.fetchone() else 1

    return _check()


def check_redis(timeout: int, retries: int) -> int:
    """Check if Redis service is available."""
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", 6379))

    @retry_with_timeout("Redis", timeout, retries)
    def _check() -> int:
        conn = redis.Redis(host=redis_host, port=redis_port)
        conn.ping()
        return 0

    return _check()


def main() -> int:
    """Main function to parse arguments and call the appropriate checks."""
    from core.config.log import LOGGING

    logging.config.dictConfig(LOGGING)
    parser = argparse.ArgumentParser(description="Healthcheck script for services.")

    parser.add_argument("--service", type=str, required=True, help="Service to check")
    parser.add_argument("--timeout", type=int, default=30, help="Maximum time (in seconds) to wait for service")
    parser.add_argument("--retries", type=int, default=5, help="Maximum number of connection retries")

    args = parser.parse_args()

    func_mapping = {
        "postgres": check_postgres,
        "redis": check_redis,
        "celery_db_table": check_db_table,
    }

    return func_mapping[args.service](args.timeout, args.retries)


if __name__ == "__main__":
    sys.exit(main())
