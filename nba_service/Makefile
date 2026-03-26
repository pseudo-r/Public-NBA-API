.PHONY: build up down restart logs shell migrate makemigrations test lint fmt check

# -----------------------------------------------
# Docker Compose
# -----------------------------------------------

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart web

logs:
	docker compose logs -f web

# -----------------------------------------------
# Django management
# -----------------------------------------------

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

shell:
	docker compose exec web python manage.py shell

createsuperuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

# -----------------------------------------------
# Ingestion shortcuts
# -----------------------------------------------

ingest-teams:
	curl -s -X POST http://localhost:8001/api/v1/ingest/teams/ | python -m json.tool

ingest-players:
	curl -s -X POST http://localhost:8001/api/v1/ingest/players/ \
	  -H "Content-Type: application/json" \
	  -d '{"season":"2024-25","is_only_current":false}' | python -m json.tool

ingest-standings:
	curl -s -X POST http://localhost:8001/api/v1/ingest/standings/ \
	  -H "Content-Type: application/json" \
	  -d '{"season":"2024-25","season_type":"Regular Season"}' | python -m json.tool

ingest-scoreboard:
	curl -s -X POST http://localhost:8001/api/v1/ingest/scoreboard/ \
	  -H "Content-Type: application/json" \
	  -d "{\"game_date\":\"$$(date +%Y-%m-%d)\"}" | python -m json.tool

ingest-player-stats:
	curl -s -X POST http://localhost:8001/api/v1/ingest/player-stats/ \
	  -H "Content-Type: application/json" \
	  -d '{"season":"2024-25","season_type":"Regular Season","measure_type":"Base","per_mode":"PerGame"}' | python -m json.tool

# -----------------------------------------------
# Testing & linting
# -----------------------------------------------

test:
	docker compose exec web pytest

test-local:
	DJANGO_SETTINGS_MODULE=config.settings.test pytest

lint:
	ruff check .

fmt:
	ruff format .

check:
	docker compose exec web python manage.py check
