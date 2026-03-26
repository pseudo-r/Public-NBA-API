"""Views for NBA data ingestion trigger endpoints."""

from datetime import date

import structlog
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingest.serializers import (
    IngestionResultSerializer,
    IngestPlayerGameLogRequestSerializer,
    IngestPlayerStatsRequestSerializer,
    IngestPlayersRequestSerializer,
    IngestScoreboardRequestSerializer,
    IngestStandingsRequestSerializer,
    IngestTeamStatsRequestSerializer,
)
from apps.ingest.services import (
    PlayerGameLogIngestionService,
    PlayerIngestionService,
    PlayerStatsIngestionService,
    ScoreboardIngestionService,
    StandingsIngestionService,
    TeamIngestionService,
    TeamStatsIngestionService,
)

logger = structlog.get_logger(__name__)


class IngestScoreboardView(APIView):
    """Trigger scoreboard ingestion for a date."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest scoreboard",
        description=(
            "Fetch scoreboard data from stats.nba.com/stats/scoreboardv2 for a given date "
            "and upsert Games into the database. Defaults to today if date not provided."
        ),
        request=IngestScoreboardRequestSerializer,
        responses={200: IngestionResultSerializer, 400: None, 502: None},
    )
    def post(self, request: Request) -> Response:
        serializer = IngestScoreboardRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        game_date = serializer.validated_data.get("game_date") or date.today()
        game_date_str = game_date.isoformat() if hasattr(game_date, "isoformat") else str(game_date)

        logger.info("scoreboard_ingest_requested", game_date=game_date_str)
        result = ScoreboardIngestionService().ingest_scoreboard(game_date_str)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestTeamsView(APIView):
    """Trigger team list ingestion."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest teams",
        description="Fetch all NBA team IDs from commonteamyears and upsert Teams.",
        responses={200: IngestionResultSerializer, 502: None},
    )
    def post(self, request: Request) -> Response:  # noqa: ARG002
        logger.info("teams_ingest_requested")
        result = TeamIngestionService().ingest_teams()
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestPlayersView(APIView):
    """Trigger player ingestion for a season."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest players",
        description="Fetch all NBA players from commonallplayers for a season and upsert Players.",
        request=IngestPlayersRequestSerializer,
        responses={200: IngestionResultSerializer, 400: None, 502: None},
    )
    def post(self, request: Request) -> Response:
        serializer = IngestPlayersRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        season = serializer.validated_data["season"]
        is_only_current = serializer.validated_data.get("is_only_current", False)

        logger.info("players_ingest_requested", season=season)
        result = PlayerIngestionService().ingest_players(season, is_only_current=is_only_current)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestStandingsView(APIView):
    """Trigger standings ingestion for a season."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest standings",
        description="Fetch standings from leaguestandingsv3 and upsert TeamStanding records.",
        request=IngestStandingsRequestSerializer,
        responses={200: IngestionResultSerializer, 400: None, 502: None},
    )
    def post(self, request: Request) -> Response:
        serializer = IngestStandingsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        season = serializer.validated_data["season"]
        season_type = serializer.validated_data.get("season_type", "Regular Season")

        logger.info("standings_ingest_requested", season=season, season_type=season_type)
        result = StandingsIngestionService().ingest_standings(season, season_type)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestPlayerGameLogView(APIView):
    """Trigger game log ingestion for a specific player."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest player game log",
        description=(
            "Fetch game-by-game stats for a player from playergamelog "
            "and upsert PlayerGameLog records."
        ),
        request=IngestPlayerGameLogRequestSerializer,
        responses={200: IngestionResultSerializer, 400: None, 502: None},
    )
    def post(self, request: Request) -> Response:
        serializer = IngestPlayerGameLogRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        player_id = serializer.validated_data["player_id"]
        season = serializer.validated_data["season"]
        season_type = serializer.validated_data.get("season_type", "Regular Season")

        logger.info("game_log_ingest_requested", player_id=player_id, season=season)
        result = PlayerGameLogIngestionService().ingest_game_log(player_id, season, season_type)
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestPlayerStatsView(APIView):
    """Trigger league-wide player stats ingestion."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest player season stats",
        description=(
            "Fetch aggregated player stats from leaguedashplayerstats "
            "and upsert PlayerSeasonStats records."
        ),
        request=IngestPlayerStatsRequestSerializer,
        responses={200: IngestionResultSerializer, 400: None, 502: None},
    )
    def post(self, request: Request) -> Response:
        serializer = IngestPlayerStatsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        logger.info("player_stats_ingest_requested", **data)
        result = PlayerStatsIngestionService().ingest_player_stats(
            data["season"],
            data.get("season_type", "Regular Season"),
            data.get("measure_type", "Base"),
            data.get("per_mode", "PerGame"),
        )
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)


class IngestTeamStatsView(APIView):
    """Trigger league-wide team stats ingestion."""

    @extend_schema(
        tags=["Ingest"],
        summary="Ingest team season stats",
        description=(
            "Fetch aggregated team stats from leaguedashteamstats "
            "and upsert TeamSeasonStats records."
        ),
        request=IngestTeamStatsRequestSerializer,
        responses={200: IngestionResultSerializer, 400: None, 502: None},
    )
    def post(self, request: Request) -> Response:
        serializer = IngestTeamStatsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        logger.info("team_stats_ingest_requested", **data)
        result = TeamStatsIngestionService().ingest_team_stats(
            data["season"],
            data.get("season_type", "Regular Season"),
            data.get("measure_type", "Base"),
            data.get("per_mode", "PerGame"),
        )
        return Response(IngestionResultSerializer(result.to_dict()).data, status=status.HTTP_200_OK)
