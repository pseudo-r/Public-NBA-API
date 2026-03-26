"""ViewSets for NBA data API endpoints."""

from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.nba.filters import (
    GameFilter,
    PlayerGameLogFilter,
    PlayerSeasonStatsFilter,
    TeamSeasonStatsFilter,
)
from apps.nba.models import (
    Game,
    Player,
    PlayerGameLog,
    PlayerSeasonStats,
    Team,
    TeamSeasonStats,
    TeamStanding,
)
from apps.nba.serializers import (
    GameListSerializer,
    GameSerializer,
    PlayerGameLogSerializer,
    PlayerListSerializer,
    PlayerSeasonStatsSerializer,
    PlayerSerializer,
    TeamListSerializer,
    TeamSeasonStatsSerializer,
    TeamSerializer,
    TeamStandingSerializer,
)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for NBA Team data."""

    search_fields = ["full_name", "abbreviation", "city", "nickname"]
    ordering_fields = ["full_name", "abbreviation", "conference", "division"]
    ordering = ["full_name"]

    def get_queryset(self) -> QuerySet[Team]:
        qs = Team.objects.all()
        conference = self.request.query_params.get("conference")
        if conference:
            qs = qs.filter(conference__iexact=conference)
        division = self.request.query_params.get("division")
        if division:
            qs = qs.filter(division__iexact=division)
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == "true")
        return qs

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return TeamListSerializer
        return TeamSerializer

    @extend_schema(
        tags=["Teams"],
        summary="List NBA teams",
        parameters=[
            OpenApiParameter("conference", description="Filter by conference (East/West)", type=str),
            OpenApiParameter("division", description="Filter by division name", type=str),
            OpenApiParameter("is_active", description="Filter active teams (true/false)", type=str),
            OpenApiParameter("search", description="Search team name/abbreviation/city", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Teams"], summary="Get team details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Teams"],
        summary="Look up team by NBA ID",
        parameters=[OpenApiParameter("nba_id", location=OpenApiParameter.PATH, type=str)],
    )
    @action(detail=False, methods=["get"], url_path="nba/(?P<nba_id>[^/.]+)")
    def by_nba_id(self, request: Request, nba_id: str) -> Response:  # noqa: ARG002
        team = self.get_queryset().filter(nba_id=nba_id).first()
        if not team:
            return Response({"error": "Team not found"}, status=404)
        return Response(TeamSerializer(team).data)


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for NBA Player data."""

    filterset_class = None  # Manual filtering for simplicity
    search_fields = ["full_name", "first_name", "last_name"]
    ordering_fields = ["full_name", "team_abbreviation", "position"]
    ordering = ["last_name", "first_name"]

    def get_queryset(self) -> QuerySet[Player]:
        return Player.objects.select_related("team")

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return PlayerListSerializer
        return PlayerSerializer

    @extend_schema(
        tags=["Players"],
        summary="List NBA players",
        parameters=[
            OpenApiParameter("team", description="Filter by team abbreviation (e.g., LAL)", type=str),
            OpenApiParameter("position", description="Filter by position (G, F, C, etc.)", type=str),
            OpenApiParameter("country", description="Filter by country", type=str),
            OpenApiParameter("is_active", description="Filter active players (true/false)", type=str),
            OpenApiParameter("search", description="Search player name", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        qs = self.get_queryset()
        team = request.query_params.get("team")
        if team:
            qs = qs.filter(team_abbreviation__iexact=team)
        position = request.query_params.get("position")
        if position:
            qs = qs.filter(position__icontains=position)
        country = request.query_params.get("country")
        if country:
            qs = qs.filter(country__iexact=country)
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == "true")
        self.queryset = qs
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Players"], summary="Get player details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Players"],
        summary="Look up player by NBA ID",
        parameters=[OpenApiParameter("nba_id", location=OpenApiParameter.PATH, type=str)],
    )
    @action(detail=False, methods=["get"], url_path="nba/(?P<nba_id>[^/.]+)")
    def by_nba_id(self, request: Request, nba_id: str) -> Response:  # noqa: ARG002
        player = Player.objects.filter(nba_id=nba_id).first()
        if not player:
            return Response({"error": "Player not found"}, status=404)
        return Response(PlayerSerializer(player).data)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for NBA Game / scoreboard data."""

    filterset_class = GameFilter
    search_fields = ["nba_id", "home_team_abbreviation", "away_team_abbreviation"]
    ordering_fields = ["game_date", "created_at"]
    ordering = ["-game_date"]

    def get_queryset(self) -> QuerySet[Game]:
        return Game.objects.select_related("home_team", "away_team")

    def get_serializer_class(self) -> type:
        if self.action == "list":
            return GameListSerializer
        return GameSerializer

    @extend_schema(
        tags=["Games"],
        summary="List games",
        parameters=[
            OpenApiParameter("season", description="Season string (e.g., 2024-25)", type=str),
            OpenApiParameter("season_type", description="Regular Season / Playoffs / Pre Season", type=str),
            OpenApiParameter("status", description="scheduled / in_progress / final", type=str),
            OpenApiParameter("date", description="Exact game date (YYYY-MM-DD)", type=str),
            OpenApiParameter("date_from", description="Games on or after (YYYY-MM-DD)", type=str),
            OpenApiParameter("date_to", description="Games on or before (YYYY-MM-DD)", type=str),
            OpenApiParameter("home_team", description="Home team abbreviation", type=str),
            OpenApiParameter("away_team", description="Away team abbreviation", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Games"], summary="Get game details")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Games"],
        summary="Look up game by NBA Game ID",
        parameters=[OpenApiParameter("nba_id", location=OpenApiParameter.PATH, type=str)],
    )
    @action(detail=False, methods=["get"], url_path="nba/(?P<nba_id>[^/.]+)")
    def by_nba_id(self, request: Request, nba_id: str) -> Response:  # noqa: ARG002
        game = self.get_queryset().filter(nba_id=nba_id).first()
        if not game:
            return Response({"error": "Game not found"}, status=404)
        return Response(GameSerializer(game).data)


class PlayerGameLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for player game logs (game-by-game stats)."""

    serializer_class = PlayerGameLogSerializer
    filterset_class = PlayerGameLogFilter
    ordering_fields = ["game_date", "pts", "reb", "ast"]
    ordering = ["-game_date"]

    def get_queryset(self) -> QuerySet[PlayerGameLog]:
        return PlayerGameLog.objects.select_related("player", "team", "game")

    @extend_schema(
        tags=["Game Logs"],
        summary="List player game logs",
        parameters=[
            OpenApiParameter("player_id", description="NBA player ID", type=str),
            OpenApiParameter("season", description="Season string (e.g., 2024-25)", type=str),
            OpenApiParameter("team", description="Team abbreviation", type=str),
            OpenApiParameter("date_from", description="On or after (YYYY-MM-DD)", type=str),
            OpenApiParameter("date_to", description="On or before (YYYY-MM-DD)", type=str),
            OpenApiParameter("wl", description="W or L", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Game Logs"], summary="Get game log entry detail")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)


class TeamStandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for NBA standings."""

    serializer_class = TeamStandingSerializer
    ordering_fields = ["conference_rank", "league_rank", "win_pct"]
    ordering = ["conference", "conference_rank"]

    def get_queryset(self) -> QuerySet[TeamStanding]:
        qs = TeamStanding.objects.select_related("team")
        season = self.request.query_params.get("season")
        if season:
            qs = qs.filter(season__iexact=season)
        season_type = self.request.query_params.get("season_type")
        if season_type:
            qs = qs.filter(season_type__iexact=season_type)
        conference = self.request.query_params.get("conference")
        if conference:
            qs = qs.filter(conference__iexact=conference)
        return qs

    @extend_schema(
        tags=["Standings"],
        summary="List standings",
        parameters=[
            OpenApiParameter("season", description="Season string (e.g., 2024-25)", type=str),
            OpenApiParameter("season_type", description="Regular Season / Playoffs", type=str),
            OpenApiParameter("conference", description="East or West", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Standings"], summary="Get standing detail")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)


class PlayerSeasonStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for aggregated player season statistics."""

    serializer_class = PlayerSeasonStatsSerializer
    filterset_class = PlayerSeasonStatsFilter
    search_fields = ["player_name"]
    ordering_fields = ["season", "player_name"]
    ordering = ["-season", "player_name"]

    def get_queryset(self) -> QuerySet[PlayerSeasonStats]:
        return PlayerSeasonStats.objects.select_related("player", "team")

    @extend_schema(
        tags=["Player Stats"],
        summary="List player season stats",
        parameters=[
            OpenApiParameter("player_id", description="NBA player ID", type=str),
            OpenApiParameter("season", description="Season string (e.g., 2024-25)", type=str),
            OpenApiParameter("season_type", description="Regular Season / Playoffs", type=str),
            OpenApiParameter("measure_type", description="Base / Advanced / Misc / Defense / Usage", type=str),
            OpenApiParameter("per_mode", description="PerGame / Totals / Per100Possessions", type=str),
            OpenApiParameter("team", description="Team abbreviation", type=str),
            OpenApiParameter("search", description="Search player name", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Player Stats"], summary="Get player stat row detail")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)


class TeamSeasonStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for aggregated team season statistics."""

    serializer_class = TeamSeasonStatsSerializer
    filterset_class = TeamSeasonStatsFilter
    search_fields = ["team_name", "team_abbreviation"]
    ordering_fields = ["season", "team_name"]
    ordering = ["-season", "team_name"]

    def get_queryset(self) -> QuerySet[TeamSeasonStats]:
        return TeamSeasonStats.objects.select_related("team")

    @extend_schema(
        tags=["Team Stats"],
        summary="List team season stats",
        parameters=[
            OpenApiParameter("team_id", description="NBA team ID", type=str),
            OpenApiParameter("season", description="Season string (e.g., 2024-25)", type=str),
            OpenApiParameter("season_type", description="Regular Season / Playoffs", type=str),
            OpenApiParameter("measure_type", description="Base / Advanced / Four Factors / Defense", type=str),
            OpenApiParameter("per_mode", description="PerGame / Totals / Per100Possessions", type=str),
            OpenApiParameter("search", description="Search team name", type=str),
        ],
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Team Stats"], summary="Get team stat row detail")
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)
