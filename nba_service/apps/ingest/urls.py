"""URL routing for ingestion trigger endpoints."""

from django.urls import path

from apps.ingest.views import (
    IngestPlayerGameLogView,
    IngestPlayerStatsView,
    IngestPlayersView,
    IngestScoreboardView,
    IngestStandingsView,
    IngestTeamStatsView,
    IngestTeamsView,
)

urlpatterns = [
    path("scoreboard/", IngestScoreboardView.as_view(), name="ingest-scoreboard"),
    path("teams/", IngestTeamsView.as_view(), name="ingest-teams"),
    path("players/", IngestPlayersView.as_view(), name="ingest-players"),
    path("standings/", IngestStandingsView.as_view(), name="ingest-standings"),
    path("game-log/", IngestPlayerGameLogView.as_view(), name="ingest-game-log"),
    path("player-stats/", IngestPlayerStatsView.as_view(), name="ingest-player-stats"),
    path("team-stats/", IngestTeamStatsView.as_view(), name="ingest-team-stats"),
]
