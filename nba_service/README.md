# NBA Django service

Django 5.2 LTS service for NBA Stats and live CDN data. See the [endpoint reference](../README.md) and [maintenance audit](../docs/audit-2026-09-30.md).

## Development

Use Python 3.12 or later in a virtual environment:

```sh
python -m pip install -e ".[dev]"
python manage.py migrate --settings=config.settings.local
python manage.py runserver --settings=config.settings.local
```

The test settings use isolated SQLite by default. CI supplies `TEST_DATABASE_URL` to exercise PostgreSQL. Run `python -m pytest` for tests and coverage. Run `python -m ruff check .` and `python -m ruff format --check .` for lint and formatting.

## Additional live routes

These GET routes return upstream JSON without persisting it:

- `/api/v1/live/scoreboard/`
- `/api/v1/live/games/{game_id}/boxscore/`
- `/api/v1/live/games/{game_id}/plays/`

Game IDs are ten-digit strings; preserve leading zeros. The CDN returns `scoreboard` or `game` objects, not Stats `resultSets`. The September 2026 probes returned HTTP 403 from this environment; client routing tests do not establish current upstream access.

Ingestion POST endpoints require an authenticated staff user in deployment. Configure secrets, database and cache URLs before starting the production image; apply migrations separately.
