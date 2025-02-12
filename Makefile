# --- Variables --------------------------------------------------------------------------------------------------------
include .env
export ENV_STATE

ENV_STATE := $(ENV_STATE:"%"=%)
DOCKER_IMAGE  = c-block-store:latest

# --- Docker -----------------------------------------------------------------------------------------------------------
.PHONY: build rebuild destroy up stop down down-v logs

rebuild: down destroy build

build:
	docker build --build-arg ENV_STATE=$(ENV_STATE) --target base -t $(DOCKER_IMAGE) .

destroy:
	docker rmi -f $(DOCKER_IMAGE)

up:
	docker compose up -d

stop:
	docker compose stop

down:
	docker compose down

down-v:
	docker compose down -v

logs:
	docker compose logs -f


# --- Django -----------------------------------------------------------------------------------------------------------
.PHONY: migrations migrate downgrade create-superuser

migrations:
	docker compose run --rm backend python manage.py makemigrations

migrate:
	docker compose run --rm backend python manage.py migrate

downgrade:
	docker exec -it backend python manage.py migrate $(word 2, $(MAKECMDGOALS)) $(word 3, $(MAKECMDGOALS))

%:  # Disable processing of arguments as file targets
	@:

create-superuser: up
	docker exec -it backend python manage.py createsuperuser

# --- Code Linters -----------------------------------------------------------------------------------------------------
.PHONY: lint flake8

lint: flake8

flake8:
	@echo "Starting flake8..."
	poetry run flake8 --toml-config=pyproject.toml .
	@echo "All done! ✨ 🍰 ✨"

# --- Code Formatters --------------------------------------------------------------------------------------------------
.PHONY: reformat isort black

reformat: isort black

isort:
	@echo "Starting isort..."
	poetry run isort --settings=pyproject.toml .

black:
	@echo "Starting black..."
	poetry run black --config=pyproject.toml .

# --- Type Checking ----------------------------------------------------------------------------------------------------
.PHONY: mypy

mypy:
	@echo "Starting type checking..."
	poetry run mypy --config-file=pyproject.toml .

# --- Pytest -----------------------------------------------------------------------------------------------------------
.PHONY: pytest pytest-cov

pytest:
	@echo "Starting pytest..."
	docker compose run --rm backend pytest
	docker compose down

pytest-cov:
	@echo "Starting pytest with coverage..."
	docker compose run --rm backend pytest --cov=. --cov-report=html
	docker compose down

# --- Code Checking ----------------------------------------------------------------------------------------------------
.PHONY: check

check:
	@echo "Start code checking..."
	$(MAKE) reformat lint mypy pytest