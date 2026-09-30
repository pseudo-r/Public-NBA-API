"""Root URL configuration for nba_service."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.core.upstream import UpstreamView

urlpatterns = [
    path("api/v1/live/scoreboard/", UpstreamView.as_view(client_method="get_live_scoreboard"), name="live-get_live_scoreboard"),
    path("api/v1/live/games/<str:game_id>/boxscore/", UpstreamView.as_view(client_method="get_live_boxscore"), name="live-get_live_boxscore"),
    path("api/v1/live/games/<str:game_id>/plays/", UpstreamView.as_view(client_method="get_live_play_by_play"), name="live-get_live_play_by_play"),

    path("admin/", admin.site.urls),
    # NBA data endpoints
    path("api/v1/", include("apps.nba.urls")),
    # Ingestion trigger endpoints
    path("api/v1/ingest/", include("apps.ingest.urls")),
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Health check
    path("healthz", include("apps.core.urls")),
]
