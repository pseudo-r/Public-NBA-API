"""DRF serializers for ingest request/response payloads."""

from rest_framework import serializers


class IngestionResultSerializer(serializers.Serializer):
    """Standard response for all ingest endpoints."""

    created = serializers.IntegerField()
    updated = serializers.IntegerField()
    errors = serializers.IntegerField()
    total_processed = serializers.IntegerField()
    details = serializers.ListField(child=serializers.CharField(), allow_empty=True)


class IngestScoreboardRequestSerializer(serializers.Serializer):
    """Request body for scoreboard ingestion."""

    game_date = serializers.DateField(
        help_text="Date to ingest (YYYY-MM-DD). Defaults to today if omitted.",
        required=False,
    )


class IngestPlayersRequestSerializer(serializers.Serializer):
    """Request body for player ingestion."""

    season = serializers.CharField(
        max_length=10,
        help_text="Season string, e.g. '2024-25'.",
    )
    is_only_current = serializers.BooleanField(
        default=False,
        help_text="If true, only return active/rostered players.",
    )


class IngestStandingsRequestSerializer(serializers.Serializer):
    """Request body for standings ingestion."""

    season = serializers.CharField(max_length=10, help_text="Season string, e.g. '2024-25'.")
    season_type = serializers.ChoiceField(
        choices=["Regular Season", "Playoffs", "Pre Season"],
        default="Regular Season",
    )


class IngestPlayerGameLogRequestSerializer(serializers.Serializer):
    """Request body for player game log ingestion."""

    player_id = serializers.IntegerField(help_text="NBA player ID.")
    season = serializers.CharField(max_length=10, help_text="Season string, e.g. '2024-25'.")
    season_type = serializers.ChoiceField(
        choices=["Regular Season", "Playoffs", "Pre Season"],
        default="Regular Season",
    )


class IngestPlayerStatsRequestSerializer(serializers.Serializer):
    """Request body for league player stats ingestion."""

    season = serializers.CharField(max_length=10)
    season_type = serializers.ChoiceField(
        choices=["Regular Season", "Playoffs", "Pre Season"],
        default="Regular Season",
    )
    measure_type = serializers.ChoiceField(
        choices=["Base", "Advanced", "Misc", "Four Factors", "Scoring", "Opponent", "Usage", "Defense"],
        default="Base",
    )
    per_mode = serializers.ChoiceField(
        choices=["PerGame", "Totals", "Per100Possessions", "Per36", "PerMinute", "PerPossession"],
        default="PerGame",
    )


class IngestTeamStatsRequestSerializer(serializers.Serializer):
    """Request body for league team stats ingestion."""

    season = serializers.CharField(max_length=10)
    season_type = serializers.ChoiceField(
        choices=["Regular Season", "Playoffs", "Pre Season"],
        default="Regular Season",
    )
    measure_type = serializers.ChoiceField(
        choices=["Base", "Advanced", "Misc", "Four Factors", "Scoring", "Opponent", "Defense"],
        default="Base",
    )
    per_mode = serializers.ChoiceField(
        choices=["PerGame", "Totals", "Per100Possessions", "Per36"],
        default="PerGame",
    )
