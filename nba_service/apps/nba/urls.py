"""URL routing for NBA data endpoints."""

from rest_framework.routers import DefaultRouter

from apps.nba.views import (
    GameViewSet,
    PlayerGameLogViewSet,
    PlayerSeasonStatsViewSet,
    PlayerViewSet,
    TeamSeasonStatsViewSet,
    TeamStandingViewSet,
    TeamViewSet,
)

router = DefaultRouter()
router.register(r"teams", TeamViewSet, basename="team")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"games", GameViewSet, basename="game")
router.register(r"game-logs", PlayerGameLogViewSet, basename="gamelog")
router.register(r"standings", TeamStandingViewSet, basename="standing")
router.register(r"player-stats", PlayerSeasonStatsViewSet, basename="player-stats")
router.register(r"team-stats", TeamSeasonStatsViewSet, basename="team-stats")

urlpatterns = router.urls
