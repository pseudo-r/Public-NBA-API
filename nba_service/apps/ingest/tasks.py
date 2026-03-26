"""Celery tasks for NBA data ingestion.

All tasks are idempotent — safe to retry or run for overlapping dates.
"""

from __future__ import annotations

from datetime import date

import structlog

from celery import shared_task

logger = structlog.get_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_scoreboard_task(self, game_date: str) -> dict:
    """Ingest scoreboard data for a specific date."""
    from apps.ingest.services import ScoreboardIngestionService

    try:
        result = ScoreboardIngestionService().ingest_scoreboard(game_date)
        logger.info("scoreboard_task_completed", game_date=game_date, **result.to_dict())
        return result.to_dict()
    except Exception as exc:
        logger.error("scoreboard_task_failed", game_date=game_date, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=2, default_retry_delay=120)
def refresh_scoreboard_today_task(self) -> dict:
    """Ingest today's scoreboard."""
    from apps.ingest.services import ScoreboardIngestionService

    try:
        today = date.today().isoformat()
        result = ScoreboardIngestionService().ingest_scoreboard(today)
        logger.info("scoreboard_today_task_completed", date=today, **result.to_dict())
        return result.to_dict()
    except Exception as exc:
        logger.error("scoreboard_today_task_failed", error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_teams_task(self) -> dict:
    """Ingest all NBA teams from commonteamyears."""
    from apps.ingest.services import TeamIngestionService

    try:
        result = TeamIngestionService().ingest_teams()
        logger.info("teams_task_completed", **result.to_dict())
        return result.to_dict()
    except Exception as exc:
        logger.error("teams_task_failed", error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_players_task(self, season: str, is_only_current: bool = False) -> dict:
    """Ingest all NBA players from commonallplayers."""
    from apps.ingest.services import PlayerIngestionService

    try:
        result = PlayerIngestionService().ingest_players(season, is_only_current=is_only_current)
        logger.info("players_task_completed", season=season, **result.to_dict())
        return result.to_dict()
    except Exception as exc:
        logger.error("players_task_failed", season=season, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_standings_task(self, season: str, season_type: str = "Regular Season") -> dict:
    """Ingest NBA standings from leaguestandingsv3."""
    from apps.ingest.services import StandingsIngestionService

    try:
        result = StandingsIngestionService().ingest_standings(season, season_type)
        logger.info("standings_task_completed", season=season, **result.to_dict())
        return result.to_dict()
    except Exception as exc:
        logger.error("standings_task_failed", season=season, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_player_game_log_task(
    self, player_id: int, season: str, season_type: str = "Regular Season"
) -> dict:
    """Ingest game log for a specific player."""
    from apps.ingest.services import PlayerGameLogIngestionService

    try:
        result = PlayerGameLogIngestionService().ingest_game_log(player_id, season, season_type)
        logger.info("game_log_task_completed", player_id=player_id, season=season, **result.to_dict())
        return result.to_dict()
    except Exception as exc:
        logger.error("game_log_task_failed", player_id=player_id, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_player_stats_task(
    self,
    season: str,
    season_type: str = "Regular Season",
    measure_type: str = "Base",
    per_mode: str = "PerGame",
) -> dict:
    """Ingest all-player season stats from leaguedashplayerstats."""
    from apps.ingest.services import PlayerStatsIngestionService

    try:
        result = PlayerStatsIngestionService().ingest_player_stats(
            season, season_type, measure_type, per_mode
        )
        logger.info(
            "player_stats_task_completed",
            season=season,
            measure_type=measure_type,
            per_mode=per_mode,
            **result.to_dict(),
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("player_stats_task_failed", season=season, error=str(exc))
        raise self.retry(exc=exc) from exc


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_team_stats_task(
    self,
    season: str,
    season_type: str = "Regular Season",
    measure_type: str = "Base",
    per_mode: str = "PerGame",
) -> dict:
    """Ingest all-team season stats from leaguedashteamstats."""
    from apps.ingest.services import TeamStatsIngestionService

    try:
        result = TeamStatsIngestionService().ingest_team_stats(
            season, season_type, measure_type, per_mode
        )
        logger.info(
            "team_stats_task_completed",
            season=season,
            measure_type=measure_type,
            per_mode=per_mode,
            **result.to_dict(),
        )
        return result.to_dict()
    except Exception as exc:
        logger.error("team_stats_task_failed", season=season, error=str(exc))
        raise self.retry(exc=exc) from exc
