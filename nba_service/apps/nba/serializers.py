"""DRF serializers for NBA data models."""

from rest_framework import serializers

from apps.nba.models import (
    Game,
    Player,
    PlayerGameLog,
    PlayerSeasonStats,
    Team,
    TeamSeasonStats,
    TeamStanding,
)


class TeamListSerializer(serializers.ModelSerializer):
    """Lightweight team serializer for list views."""

    class Meta:
        model = Team
        fields = [
            "id",
            "nba_id",
            "abbreviation",
            "full_name",
            "nickname",
            "city",
            "conference",
            "division",
            "is_active",
        ]


class TeamSerializer(serializers.ModelSerializer):
    """Full team serializer with arena / coach / ownership details."""

    class Meta:
        model = Team
        fields = [
            "id",
            "nba_id",
            "abbreviation",
            "full_name",
            "nickname",
            "city",
            "state",
            "year_founded",
            "conference",
            "division",
            "arena",
            "arena_capacity",
            "owner",
            "general_manager",
            "head_coach",
            "dleague_affiliation",
            "is_active",
            "created_at",
            "updated_at",
        ]


class PlayerListSerializer(serializers.ModelSerializer):
    """Lightweight player serializer for list views."""

    team_name = serializers.CharField(source="team.full_name", read_only=True, default=None)

    class Meta:
        model = Player
        fields = [
            "id",
            "nba_id",
            "full_name",
            "team_abbreviation",
            "team_name",
            "position",
            "jersey",
            "is_active",
        ]


class PlayerSerializer(serializers.ModelSerializer):
    """Full player serializer."""

    team_name = serializers.CharField(source="team.full_name", read_only=True, default=None)

    class Meta:
        model = Player
        fields = [
            "id",
            "nba_id",
            "first_name",
            "last_name",
            "full_name",
            "team_abbreviation",
            "team_name",
            "position",
            "jersey",
            "height",
            "weight",
            "birth_date",
            "age",
            "country",
            "school",
            "draft_year",
            "draft_round",
            "draft_number",
            "season_exp",
            "from_year",
            "to_year",
            "is_active",
            "headshot_url",
            "created_at",
            "updated_at",
        ]


class GameListSerializer(serializers.ModelSerializer):
    """Lightweight game serializer for list views."""

    class Meta:
        model = Game
        fields = [
            "id",
            "nba_id",
            "home_team_abbreviation",
            "away_team_abbreviation",
            "home_score",
            "away_score",
            "game_date",
            "season",
            "season_type",
            "status",
            "national_tv",
        ]


class GameSerializer(serializers.ModelSerializer):
    """Full game serializer."""

    home_team_name = serializers.CharField(
        source="home_team.full_name", read_only=True, default=None
    )
    away_team_name = serializers.CharField(
        source="away_team.full_name", read_only=True, default=None
    )

    class Meta:
        model = Game
        fields = [
            "id",
            "nba_id",
            "home_team_abbreviation",
            "home_team_name",
            "away_team_abbreviation",
            "away_team_name",
            "home_score",
            "away_score",
            "game_date",
            "game_time",
            "season",
            "season_type",
            "status",
            "status_text",
            "period",
            "game_clock",
            "arena",
            "arena_city",
            "arena_state",
            "attendance",
            "game_duration",
            "national_tv",
            "created_at",
            "updated_at",
        ]


class PlayerGameLogSerializer(serializers.ModelSerializer):
    """Player game log serializer."""

    player_name = serializers.CharField(source="player.full_name", read_only=True)

    class Meta:
        model = PlayerGameLog
        fields = [
            "id",
            "player_name",
            "game_nba_id",
            "team_abbreviation",
            "matchup",
            "game_date",
            "season",
            "wl",
            "min",
            "fgm",
            "fga",
            "fg_pct",
            "fg3m",
            "fg3a",
            "fg3_pct",
            "ftm",
            "fta",
            "ft_pct",
            "oreb",
            "dreb",
            "reb",
            "ast",
            "stl",
            "blk",
            "tov",
            "pf",
            "pts",
            "plus_minus",
            "video_available",
        ]


class TeamStandingSerializer(serializers.ModelSerializer):
    """Team standing serializer."""

    team_name = serializers.CharField(source="team.full_name", read_only=True)
    team_abbreviation = serializers.CharField(source="team.abbreviation", read_only=True)

    class Meta:
        model = TeamStanding
        fields = [
            "id",
            "team_name",
            "team_abbreviation",
            "season",
            "season_type",
            "conference",
            "division",
            "wins",
            "losses",
            "win_pct",
            "home_record",
            "road_record",
            "conference_rank",
            "division_rank",
            "league_rank",
            "clinch_indicator",
            "current_streak",
            "last_ten_wins",
            "last_ten_losses",
            "pts_pg",
            "opp_pts_pg",
            "pts_diff",
            "conference_games_back",
            "division_games_back",
            "updated_at",
        ]


class PlayerSeasonStatsSerializer(serializers.ModelSerializer):
    """Player season stats serializer."""

    class Meta:
        model = PlayerSeasonStats
        fields = [
            "id",
            "player_nba_id",
            "player_name",
            "team_abbreviation",
            "season",
            "season_type",
            "measure_type",
            "per_mode",
            "age",
            "stats",
            "updated_at",
        ]


class TeamSeasonStatsSerializer(serializers.ModelSerializer):
    """Team season stats serializer."""

    class Meta:
        model = TeamSeasonStats
        fields = [
            "id",
            "team_nba_id",
            "team_name",
            "team_abbreviation",
            "season",
            "season_type",
            "measure_type",
            "per_mode",
            "stats",
            "updated_at",
        ]
