"""Django-filter filtersets for NBA data models."""

import django_filters

from apps.nba.models import Game, Player, PlayerGameLog, PlayerSeasonStats, TeamSeasonStats


class PlayerFilter(django_filters.FilterSet):
    team = django_filters.CharFilter(field_name="team_abbreviation", lookup_expr="iexact")
    position = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="iexact")
    is_active = django_filters.BooleanFilter()
    from_year = django_filters.NumberFilter()
    to_year = django_filters.NumberFilter()
    draft_year = django_filters.NumberFilter()

    class Meta:
        model = Player
        fields = ["team", "position", "country", "is_active", "from_year", "to_year", "draft_year"]


class GameFilter(django_filters.FilterSet):
    season = django_filters.CharFilter(lookup_expr="iexact")
    season_type = django_filters.CharFilter(lookup_expr="iexact")
    status = django_filters.CharFilter(lookup_expr="iexact")
    date = django_filters.DateFilter(field_name="game_date")
    date_from = django_filters.DateFilter(field_name="game_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="game_date", lookup_expr="lte")
    home_team = django_filters.CharFilter(
        field_name="home_team_abbreviation", lookup_expr="iexact"
    )
    away_team = django_filters.CharFilter(
        field_name="away_team_abbreviation", lookup_expr="iexact"
    )

    class Meta:
        model = Game
        fields = ["season", "season_type", "status", "date", "date_from", "date_to",
                  "home_team", "away_team"]


class PlayerGameLogFilter(django_filters.FilterSet):
    player_id = django_filters.CharFilter(field_name="player__nba_id", lookup_expr="exact")
    season = django_filters.CharFilter(lookup_expr="iexact")
    team = django_filters.CharFilter(field_name="team_abbreviation", lookup_expr="iexact")
    date_from = django_filters.DateFilter(field_name="game_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="game_date", lookup_expr="lte")
    wl = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = PlayerGameLog
        fields = ["player_id", "season", "team", "date_from", "date_to", "wl"]


class PlayerSeasonStatsFilter(django_filters.FilterSet):
    season = django_filters.CharFilter(lookup_expr="iexact")
    season_type = django_filters.CharFilter(lookup_expr="iexact")
    measure_type = django_filters.CharFilter(lookup_expr="iexact")
    per_mode = django_filters.CharFilter(lookup_expr="iexact")
    player_id = django_filters.CharFilter(field_name="player_nba_id", lookup_expr="exact")
    team = django_filters.CharFilter(field_name="team_abbreviation", lookup_expr="iexact")

    class Meta:
        model = PlayerSeasonStats
        fields = ["season", "season_type", "measure_type", "per_mode", "player_id", "team"]


class TeamSeasonStatsFilter(django_filters.FilterSet):
    season = django_filters.CharFilter(lookup_expr="iexact")
    season_type = django_filters.CharFilter(lookup_expr="iexact")
    measure_type = django_filters.CharFilter(lookup_expr="iexact")
    per_mode = django_filters.CharFilter(lookup_expr="iexact")
    team_id = django_filters.CharFilter(field_name="team_nba_id", lookup_expr="exact")

    class Meta:
        model = TeamSeasonStats
        fields = ["season", "season_type", "measure_type", "per_mode", "team_id"]
