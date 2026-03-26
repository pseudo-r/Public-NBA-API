"""NBA admin registrations."""

from django.contrib import admin

from apps.nba.models import (
    Game,
    Player,
    PlayerGameLog,
    PlayerSeasonStats,
    Team,
    TeamSeasonStats,
    TeamStanding,
)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["full_name", "abbreviation", "conference", "division", "is_active"]
    list_filter = ["conference", "division", "is_active"]
    search_fields = ["full_name", "abbreviation", "city"]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "team_abbreviation", "position", "jersey", "is_active"]
    list_filter = ["is_active", "position"]
    search_fields = ["full_name", "nba_id"]
    raw_id_fields = ["team"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "nba_id", "away_team_abbreviation", "home_team_abbreviation",
        "away_score", "home_score", "game_date", "season", "status",
    ]
    list_filter = ["season", "season_type", "status"]
    search_fields = ["nba_id", "home_team_abbreviation", "away_team_abbreviation"]
    date_hierarchy = "game_date"


@admin.register(PlayerGameLog)
class PlayerGameLogAdmin(admin.ModelAdmin):
    list_display = ["player", "game_nba_id", "matchup", "game_date", "pts", "reb", "ast"]
    list_filter = ["season", "wl"]
    search_fields = ["player__full_name", "game_nba_id"]
    raw_id_fields = ["player", "game", "team"]
    date_hierarchy = "game_date"


@admin.register(TeamStanding)
class TeamStandingAdmin(admin.ModelAdmin):
    list_display = [
        "team", "season", "season_type", "conference",
        "wins", "losses", "win_pct", "conference_rank",
    ]
    list_filter = ["season", "season_type", "conference"]
    raw_id_fields = ["team"]


@admin.register(PlayerSeasonStats)
class PlayerSeasonStatsAdmin(admin.ModelAdmin):
    list_display = [
        "player_name", "team_abbreviation", "season",
        "season_type", "measure_type", "per_mode",
    ]
    list_filter = ["season", "season_type", "measure_type", "per_mode"]
    search_fields = ["player_name", "player_nba_id"]


@admin.register(TeamSeasonStats)
class TeamSeasonStatsAdmin(admin.ModelAdmin):
    list_display = [
        "team_name", "team_abbreviation", "season",
        "season_type", "measure_type", "per_mode",
    ]
    list_filter = ["season", "season_type", "measure_type", "per_mode"]
    search_fields = ["team_name", "team_nba_id"]
