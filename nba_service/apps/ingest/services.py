"""Data ingestion services for NBA Stats data.

Each service fetches data from the NBA Stats API and upserts it into
the database using idempotent update_or_create operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as date_cls
from typing import Any

import structlog
from django.db import transaction

from apps.core.exceptions import IngestionError
from apps.nba.models import (
    Game,
    Player,
    PlayerGameLog,
    PlayerSeasonStats,
    Team,
    TeamSeasonStats,
    TeamStanding,
)
from clients.nba_client import NBAClientError, get_nba_client

logger = structlog.get_logger(__name__)


@dataclass
class IngestionResult:
    """Result of an ingestion operation."""

    created: int = 0
    updated: int = 0
    errors: int = 0
    details: list[str] = field(default_factory=list)

    @property
    def total_processed(self) -> int:
        return self.created + self.updated

    def to_dict(self) -> dict[str, Any]:
        return {
            "created": self.created,
            "updated": self.updated,
            "errors": self.errors,
            "total_processed": self.total_processed,
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# Team ingestion
# ---------------------------------------------------------------------------


class TeamIngestionService:
    """Ingest all NBA teams.

    Uses leaguedashteamstats (Base/PerGame) which is reliably accessible via
    the WAF and contains all 30 active team IDs, names, and abbreviations.
    """

    CURRENT_SEASON = "2024-25"

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    @transaction.atomic
    def ingest_teams(self, season: str | None = None) -> IngestionResult:
        result = IngestionResult()
        season = season or self.CURRENT_SEASON
        try:
            response = self.client.get_league_team_stats(
                season=season,
                season_type="Regular Season",
                measure_type="Base",
                per_mode="PerGame",
            )
            rows = response.named_result_set("LeagueDashTeamStats")

            if not rows:
                raise IngestionError(
                    f"No team stats rows returned for season {season}. "
                    "The NBA WAF may be blocking this request."
                )

            for row in rows:
                try:
                    nba_id = str(row.get("TEAM_ID", ""))
                    if not nba_id:
                        result.errors += 1
                        continue

                    team_name = row.get("TEAM_NAME", "")
                    abbrev = row.get("TEAM_ABBREVIATION", "")

                    _, created = Team.objects.update_or_create(
                        nba_id=nba_id,
                        defaults={
                            "abbreviation": abbrev,
                            "full_name": team_name,
                            "nickname": team_name.split()[-1] if team_name else "",
                            "is_active": True,
                            "raw_data": row,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("team_row_error", error=str(e), row=row)
                    result.errors += 1

            logger.info("teams_ingested", season=season, **result.to_dict())
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest teams: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Player ingestion
# ---------------------------------------------------------------------------


class PlayerIngestionService:
    """Ingest all NBA players from commonallplayers."""

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    def _build_headshot_url(self, nba_id: str) -> str:
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{nba_id}.png"

    @transaction.atomic
    def ingest_players(self, season: str, is_only_current: bool = False) -> IngestionResult:
        result = IngestionResult()
        try:
            response = self.client.get_all_players(season, is_only_current=is_only_current)
            rows = response.named_result_set("CommonAllPlayers")

            for row in rows:
                try:
                    nba_id = str(row.get("PERSON_ID", ""))
                    if not nba_id:
                        result.errors += 1
                        continue

                    team_id = str(row.get("TEAM_ID", "")) or None
                    team_obj = None
                    if team_id and team_id != "0":
                        team_obj = Team.objects.filter(nba_id=team_id).first()

                    full_name = row.get("DISPLAY_FIRST_LAST", "")
                    first, _, last = full_name.partition(" ")

                    _, created = Player.objects.update_or_create(
                        nba_id=nba_id,
                        defaults={
                            "first_name": first,
                            "last_name": last,
                            "full_name": full_name,
                            "display_first_last": full_name,
                            "team": team_obj,
                            "team_abbreviation": row.get("TEAM_ABBREVIATION", ""),
                            "is_active": bool(row.get("ROSTERSTATUS", 0)),
                            "from_year": row.get("FROM_YEAR"),
                            "to_year": row.get("TO_YEAR"),
                            "headshot_url": self._build_headshot_url(nba_id),
                            "raw_data": row,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("player_row_error", nba_id=nba_id, error=str(e))
                    result.errors += 1

            logger.info("players_ingested", season=season, **result.to_dict())
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest players: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Scoreboard ingestion
# ---------------------------------------------------------------------------


class ScoreboardIngestionService:
    """Ingest NBA scoreboard for a given date from scoreboardv2."""

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    def _parse_status(self, status_num: int | None, clock: str) -> str:
        if status_num == 1:
            return Game.STATUS_SCHEDULED
        if status_num == 2:
            return Game.STATUS_IN_PROGRESS
        return Game.STATUS_FINAL

    @transaction.atomic
    def ingest_scoreboard(self, game_date: str) -> IngestionResult:
        result = IngestionResult()
        try:
            response = self.client.get_scoreboard(game_date)
            game_headers = response.named_result_set("GameHeader")
            line_scores = response.named_result_set("LineScore")

            # Build score lookup: game_id → {home_team_id: score, away_team_id: score}
            score_map: dict[str, dict[str, int]] = {}
            for ls in line_scores:
                gid = str(ls.get("GAME_ID", ""))
                tid = str(ls.get("TEAM_ID", ""))
                pts = ls.get("PTS") or 0
                if gid not in score_map:
                    score_map[gid] = {}
                score_map[gid][tid] = pts

            for gh in game_headers:
                try:
                    nba_id = str(gh.get("GAME_ID", ""))
                    if not nba_id:
                        result.errors += 1
                        continue

                    home_id = str(gh.get("HOME_TEAM_ID", ""))
                    away_id = str(gh.get("VISITOR_TEAM_ID", ""))

                    home_team = Team.objects.filter(nba_id=home_id).first() if home_id else None
                    away_team = Team.objects.filter(nba_id=away_id).first() if away_id else None

                    scores = score_map.get(nba_id, {})
                    home_score = scores.get(home_id)
                    away_score = scores.get(away_id)

                    # Parse date
                    raw_date = gh.get("GAME_DATE_EST", game_date)
                    try:
                        parsed_date = date_cls.fromisoformat(raw_date[:10])
                    except (ValueError, TypeError):
                        parsed_date = date_cls.fromisoformat(game_date)

                    status = self._parse_status(gh.get("GAME_STATUS_ID"), gh.get("GAME_STATUS_TEXT", ""))

                    _, created = Game.objects.update_or_create(
                        nba_id=nba_id,
                        defaults={
                            "home_team": home_team,
                            "away_team": away_team,
                            "home_team_abbreviation": home_team.abbreviation if home_team else "",
                            "away_team_abbreviation": away_team.abbreviation if away_team else "",
                            "home_score": home_score,
                            "away_score": away_score,
                            "game_date": parsed_date,
                            "game_date_est": raw_date,
                            "season": gh.get("SEASON", ""),
                            "season_type": Game.SEASON_TYPE_REGULAR,
                            "status": status,
                            "status_text": gh.get("GAME_STATUS_TEXT", ""),
                            "arena": gh.get("ARENA_NAME", ""),
                            "national_tv": gh.get("NATL_TV_BROADCASTER_ABBREVIATION", ""),
                            "raw_data": gh,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("game_row_error", game_id=gh.get("GAME_ID"), error=str(e))
                    result.errors += 1

            logger.info("scoreboard_ingested", game_date=game_date, **result.to_dict())
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest scoreboard for {game_date}: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Standings ingestion
# ---------------------------------------------------------------------------


class StandingsIngestionService:
    """Ingest league standings from leaguestandingsv3."""

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    @transaction.atomic
    def ingest_standings(self, season: str, season_type: str = "Regular Season") -> IngestionResult:
        result = IngestionResult()
        try:
            response = self.client.get_standings(season, season_type)
            rows = response.named_result_set("Standings")

            for row in rows:
                try:
                    team_id = str(row.get("TeamID", ""))
                    if not team_id:
                        result.errors += 1
                        continue

                    team_obj = Team.objects.filter(nba_id=team_id).first()
                    if not team_obj:
                        # Create a stub
                        team_obj, _ = Team.objects.get_or_create(
                            nba_id=team_id,
                            defaults={
                                "abbreviation": row.get("TeamSlug", team_id)[:5],
                                "full_name": row.get("TeamName", team_id),
                                "conference": row.get("Conference", ""),
                                "division": row.get("Division", ""),
                            },
                        )

                    home_w = row.get("HOME_W", 0) or 0
                    home_l = row.get("HOME_L", 0) or 0
                    road_w = row.get("ROAD_W", 0) or 0
                    road_l = row.get("ROAD_L", 0) or 0

                    _, created = TeamStanding.objects.update_or_create(
                        team=team_obj,
                        season=season,
                        season_type=season_type,
                        defaults={
                            "wins": row.get("WINS", 0) or 0,
                            "losses": row.get("LOSSES", 0) or 0,
                            "win_pct": row.get("WinPct"),
                            "home_record": f"{home_w}-{home_l}",
                            "road_record": f"{road_w}-{road_l}",
                            "conference_rank": row.get("ConferenceRank"),
                            "division_rank": row.get("DivisionRank"),
                            "league_rank": row.get("LeagueRank"),
                            "conference": row.get("Conference", ""),
                            "division": row.get("Division", ""),
                            "clinch_indicator": row.get("ClinchIndicator", ""),
                            "current_streak": str(row.get("CurrentStreak", "")),
                            "last_ten_wins": row.get("L10_W"),
                            "last_ten_losses": row.get("L10_L"),
                            "pts_pg": row.get("PointsPG"),
                            "opp_pts_pg": row.get("OppPointsPG"),
                            "pts_diff": row.get("DiffPointsPG"),
                            "conference_games_back": str(row.get("ConferenceGamesBack", "")),
                            "division_games_back": str(row.get("DivisionGamesBack", "")),
                            "raw_data": row,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("standing_row_error", team_id=team_id, error=str(e))
                    result.errors += 1

            logger.info("standings_ingested", season=season, **result.to_dict())
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest standings: {e}") from e

        return result


# ---------------------------------------------------------------------------
# Player game log ingestion
# ---------------------------------------------------------------------------


class PlayerGameLogIngestionService:
    """Ingest game log for a single player from playergamelog."""

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    @transaction.atomic
    def ingest_game_log(
        self,
        player_id: int,
        season: str,
        season_type: str = "Regular Season",
    ) -> IngestionResult:
        result = IngestionResult()
        try:
            player_obj = Player.objects.filter(nba_id=str(player_id)).first()
            if not player_obj:
                raise IngestionError(f"Player {player_id} not found in database. Ingest players first.")

            response = self.client.get_player_game_log(player_id, season, season_type)
            rows = response.named_result_set("PlayerGameLog")

            for row in rows:
                try:
                    game_nba_id = str(row.get("Game_ID", ""))
                    if not game_nba_id:
                        result.errors += 1
                        continue

                    team_abbr = row.get("TEAM_ABBREVIATION", "")
                    team_obj = Team.objects.filter(abbreviation__iexact=team_abbr).first()
                    game_obj = Game.objects.filter(nba_id=game_nba_id).first()

                    raw_date = row.get("GAME_DATE", "")
                    try:
                        game_date = date_cls.fromisoformat(raw_date)
                    except (ValueError, TypeError):
                        game_date = None

                    _, created = PlayerGameLog.objects.update_or_create(
                        player=player_obj,
                        game_nba_id=game_nba_id,
                        defaults={
                            "game": game_obj,
                            "team": team_obj,
                            "team_abbreviation": team_abbr,
                            "matchup": row.get("MATCHUP", ""),
                            "game_date": game_date,
                            "season": season,
                            "wl": row.get("WL", ""),
                            "min": str(row.get("MIN", "")),
                            "fgm": row.get("FGM"),
                            "fga": row.get("FGA"),
                            "fg_pct": row.get("FG_PCT"),
                            "fg3m": row.get("FG3M"),
                            "fg3a": row.get("FG3A"),
                            "fg3_pct": row.get("FG3_PCT"),
                            "ftm": row.get("FTM"),
                            "fta": row.get("FTA"),
                            "ft_pct": row.get("FT_PCT"),
                            "oreb": row.get("OREB"),
                            "dreb": row.get("DREB"),
                            "reb": row.get("REB"),
                            "ast": row.get("AST"),
                            "stl": row.get("STL"),
                            "blk": row.get("BLK"),
                            "tov": row.get("TOV"),
                            "pf": row.get("PF"),
                            "pts": row.get("PTS"),
                            "plus_minus": row.get("PLUS_MINUS"),
                            "video_available": bool(row.get("VIDEO_AVAILABLE", 0)),
                            "raw_data": row,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("gamelog_row_error", game_id=game_nba_id, error=str(e))
                    result.errors += 1

            logger.info(
                "game_log_ingested",
                player_id=player_id,
                season=season,
                **result.to_dict(),
            )
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest game log for player {player_id}: {e}") from e

        return result


# ---------------------------------------------------------------------------
# League player stats ingestion
# ---------------------------------------------------------------------------


class PlayerStatsIngestionService:
    """Ingest aggregated player season stats from leaguedashplayerstats."""

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    @transaction.atomic
    def ingest_player_stats(
        self,
        season: str,
        season_type: str = "Regular Season",
        measure_type: str = "Base",
        per_mode: str = "PerGame",
    ) -> IngestionResult:
        result = IngestionResult()
        try:
            response = self.client.get_league_player_stats(
                season, season_type, measure_type, per_mode
            )
            rows = response.named_result_set("LeagueDashPlayerStats")

            for row in rows:
                try:
                    player_id = str(row.get("PLAYER_ID", ""))
                    if not player_id:
                        result.errors += 1
                        continue

                    player_obj = Player.objects.filter(nba_id=player_id).first()
                    team_abbr = row.get("TEAM_ABBREVIATION", "")
                    team_obj = Team.objects.filter(abbreviation__iexact=team_abbr).first()

                    # Extract the most analytical columns as top-level stats
                    stats = {k: v for k, v in row.items() if k not in (
                        "PLAYER_ID", "PLAYER_NAME", "PLAYER_NAME_LAST_FIRST",
                        "TEAM_ID", "TEAM_ABBREVIATION", "AGE",
                    )}

                    _, created = PlayerSeasonStats.objects.update_or_create(
                        player_nba_id=player_id,
                        season=season,
                        season_type=season_type,
                        measure_type=measure_type,
                        per_mode=per_mode,
                        defaults={
                            "player": player_obj,
                            "team": team_obj,
                            "player_name": row.get("PLAYER_NAME", ""),
                            "team_abbreviation": team_abbr,
                            "age": row.get("AGE"),
                            "stats": stats,
                            "raw_data": row,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("player_stats_row_error", player_id=player_id, error=str(e))
                    result.errors += 1

            logger.info(
                "player_stats_ingested",
                season=season,
                measure_type=measure_type,
                per_mode=per_mode,
                **result.to_dict(),
            )
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest player stats: {e}") from e

        return result


# ---------------------------------------------------------------------------
# League team stats ingestion
# ---------------------------------------------------------------------------


class TeamStatsIngestionService:
    """Ingest aggregated team season stats from leaguedashteamstats."""

    def __init__(self, client=None):
        self.client = client or get_nba_client()

    @transaction.atomic
    def ingest_team_stats(
        self,
        season: str,
        season_type: str = "Regular Season",
        measure_type: str = "Base",
        per_mode: str = "PerGame",
    ) -> IngestionResult:
        result = IngestionResult()
        try:
            response = self.client.get_league_team_stats(
                season, season_type, measure_type, per_mode
            )
            rows = response.named_result_set("LeagueDashTeamStats")

            for row in rows:
                try:
                    team_id = str(row.get("TEAM_ID", ""))
                    if not team_id:
                        result.errors += 1
                        continue

                    team_obj = Team.objects.filter(nba_id=team_id).first()
                    team_abbr = row.get("TEAM_ABBREVIATION", "")

                    stats = {k: v for k, v in row.items() if k not in (
                        "TEAM_ID", "TEAM_NAME", "TEAM_ABBREVIATION",
                        "CFID", "CFPARAMS",
                    )}

                    _, created = TeamSeasonStats.objects.update_or_create(
                        team_nba_id=team_id,
                        season=season,
                        season_type=season_type,
                        measure_type=measure_type,
                        per_mode=per_mode,
                        defaults={
                            "team": team_obj,
                            "team_name": row.get("TEAM_NAME", ""),
                            "team_abbreviation": team_abbr,
                            "stats": stats,
                            "raw_data": row,
                        },
                    )
                    if created:
                        result.created += 1
                    else:
                        result.updated += 1
                except Exception as e:
                    logger.error("team_stats_row_error", team_id=team_id, error=str(e))
                    result.errors += 1

            logger.info(
                "team_stats_ingested",
                season=season,
                measure_type=measure_type,
                per_mode=per_mode,
                **result.to_dict(),
            )
        except NBAClientError as e:
            raise IngestionError(f"Failed to ingest team stats: {e}") from e

        return result
