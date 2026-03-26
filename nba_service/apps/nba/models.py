"""Database models for NBA Stats data."""

from django.db import models


class TimestampMixin(models.Model):
    """Mixin providing created_at and updated_at timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Team(TimestampMixin):
    """NBA team entity."""

    CONFERENCE_EAST = "East"
    CONFERENCE_WEST = "West"
    CONFERENCE_CHOICES = [
        (CONFERENCE_EAST, "Eastern Conference"),
        (CONFERENCE_WEST, "Western Conference"),
    ]

    nba_id = models.CharField(max_length=20, unique=True, db_index=True)
    abbreviation = models.CharField(max_length=5, db_index=True)
    full_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, blank=True)  # e.g., "Lakers"
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    year_founded = models.PositiveSmallIntegerField(null=True, blank=True)
    conference = models.CharField(
        max_length=10, choices=CONFERENCE_CHOICES, blank=True, db_index=True
    )
    division = models.CharField(max_length=50, blank=True, db_index=True)
    arena = models.CharField(max_length=100, blank=True)
    arena_capacity = models.PositiveIntegerField(null=True, blank=True)
    owner = models.CharField(max_length=100, blank=True)
    general_manager = models.CharField(max_length=100, blank=True)
    head_coach = models.CharField(max_length=100, blank=True)
    dleague_affiliation = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name


class Player(TimestampMixin):
    """NBA player entity."""

    POSITION_GUARD = "G"
    POSITION_FORWARD = "F"
    POSITION_CENTER = "C"
    POSITION_FORWARD_GUARD = "F-G"
    POSITION_FORWARD_CENTER = "F-C"
    POSITION_CENTER_FORWARD = "C-F"
    POSITION_GUARD_FORWARD = "G-F"

    nba_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, db_index=True)
    display_first_last = models.CharField(max_length=100, blank=True)

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
    )
    team_abbreviation = models.CharField(max_length=5, blank=True)

    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    from_year = models.PositiveSmallIntegerField(null=True, blank=True)
    to_year = models.PositiveSmallIntegerField(null=True, blank=True)

    # Position & jersey
    position = models.CharField(max_length=10, blank=True, db_index=True)
    jersey = models.CharField(max_length=5, blank=True)

    # Physical
    height = models.CharField(max_length=10, blank=True)  # e.g., "6-9"
    weight = models.CharField(max_length=10, blank=True)  # in lbs
    birth_date = models.DateField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    school = models.CharField(max_length=100, blank=True)

    # Draft
    draft_year = models.PositiveSmallIntegerField(null=True, blank=True)
    draft_round = models.PositiveSmallIntegerField(null=True, blank=True)
    draft_number = models.PositiveSmallIntegerField(null=True, blank=True)

    # Season type
    season_exp = models.PositiveSmallIntegerField(null=True, blank=True)

    # Media
    headshot_url = models.URLField(max_length=500, blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return self.full_name


class Game(TimestampMixin):
    """NBA game entity."""

    SEASON_TYPE_PRESEASON = "Pre Season"
    SEASON_TYPE_REGULAR = "Regular Season"
    SEASON_TYPE_PLAYOFFS = "Playoffs"
    SEASON_TYPE_ALLSTAR = "All Star"
    SEASON_TYPE_CHOICES = [
        (SEASON_TYPE_PRESEASON, "Pre Season"),
        (SEASON_TYPE_REGULAR, "Regular Season"),
        (SEASON_TYPE_PLAYOFFS, "Playoffs"),
        (SEASON_TYPE_ALLSTAR, "All Star"),
    ]

    STATUS_SCHEDULED = "scheduled"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_FINAL = "final"
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_FINAL, "Final"),
    ]

    nba_id = models.CharField(max_length=15, unique=True, db_index=True)  # e.g., 0022401063
    home_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_games",
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="away_games",
    )
    home_team_abbreviation = models.CharField(max_length=5, blank=True)
    away_team_abbreviation = models.CharField(max_length=5, blank=True)

    game_date = models.DateField(db_index=True)
    game_date_est = models.CharField(max_length=20, blank=True)  # Raw EST string from API
    game_time = models.CharField(max_length=10, blank=True)

    season = models.CharField(max_length=10, db_index=True)  # e.g., "2024-25"
    season_type = models.CharField(
        max_length=20, choices=SEASON_TYPE_CHOICES, default=SEASON_TYPE_REGULAR, db_index=True
    )

    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_SCHEDULED, db_index=True
    )
    status_text = models.CharField(max_length=50, blank=True)

    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)

    period = models.PositiveSmallIntegerField(null=True, blank=True)
    game_clock = models.CharField(max_length=10, blank=True)

    arena = models.CharField(max_length=100, blank=True)
    arena_city = models.CharField(max_length=50, blank=True)
    arena_state = models.CharField(max_length=50, blank=True)

    attendance = models.PositiveIntegerField(null=True, blank=True)
    game_duration = models.CharField(max_length=10, blank=True)

    national_tv = models.CharField(max_length=50, blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-game_date", "nba_id"]

    def __str__(self) -> str:
        return (
            f"{self.away_team_abbreviation} @ {self.home_team_abbreviation} "
            f"({self.game_date})"
        )


class PlayerGameLog(TimestampMixin):
    """Single player's stats for a specific game (game log row)."""

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="game_logs",
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="player_logs",
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="player_game_logs",
    )

    # Identifiers for orphan resolution
    game_nba_id = models.CharField(max_length=15, db_index=True)
    team_abbreviation = models.CharField(max_length=5, blank=True)
    matchup = models.CharField(max_length=20, blank=True)  # e.g., "LAL vs. BOS"
    game_date = models.DateField(db_index=True)

    season = models.CharField(max_length=10, db_index=True)

    # Result
    wl = models.CharField(max_length=1, blank=True)  # 'W' or 'L'

    # Box score stats
    min = models.CharField(max_length=10, blank=True)
    fgm = models.SmallIntegerField(null=True, blank=True)
    fga = models.SmallIntegerField(null=True, blank=True)
    fg_pct = models.FloatField(null=True, blank=True)
    fg3m = models.SmallIntegerField(null=True, blank=True)
    fg3a = models.SmallIntegerField(null=True, blank=True)
    fg3_pct = models.FloatField(null=True, blank=True)
    ftm = models.SmallIntegerField(null=True, blank=True)
    fta = models.SmallIntegerField(null=True, blank=True)
    ft_pct = models.FloatField(null=True, blank=True)
    oreb = models.SmallIntegerField(null=True, blank=True)
    dreb = models.SmallIntegerField(null=True, blank=True)
    reb = models.SmallIntegerField(null=True, blank=True)
    ast = models.SmallIntegerField(null=True, blank=True)
    stl = models.SmallIntegerField(null=True, blank=True)
    blk = models.SmallIntegerField(null=True, blank=True)
    tov = models.SmallIntegerField(null=True, blank=True)
    pf = models.SmallIntegerField(null=True, blank=True)
    pts = models.SmallIntegerField(null=True, blank=True)
    plus_minus = models.SmallIntegerField(null=True, blank=True)
    video_available = models.BooleanField(default=False)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-game_date"]
        unique_together = [["player", "game_nba_id"]]

    def __str__(self) -> str:
        return f"{self.player.full_name} — {self.matchup} ({self.game_date})"


class TeamStanding(TimestampMixin):
    """Team standings for a given season and season type."""

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="standings",
    )
    season = models.CharField(max_length=10, db_index=True)
    season_type = models.CharField(max_length=20, db_index=True)

    # Record
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    win_pct = models.FloatField(null=True, blank=True)
    home_record = models.CharField(max_length=10, blank=True)
    road_record = models.CharField(max_length=10, blank=True)

    # Rankings
    conference_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    division_rank = models.PositiveSmallIntegerField(null=True, blank=True)
    league_rank = models.PositiveSmallIntegerField(null=True, blank=True)

    # Conference / division
    conference = models.CharField(max_length=10, blank=True, db_index=True)
    division = models.CharField(max_length=50, blank=True)

    # Clinch
    clinch_indicator = models.CharField(max_length=10, blank=True)

    # Streaks / recent
    current_streak = models.CharField(max_length=10, blank=True)
    last_ten_wins = models.PositiveSmallIntegerField(null=True, blank=True)
    last_ten_losses = models.PositiveSmallIntegerField(null=True, blank=True)

    # Point differential
    pts_pg = models.FloatField(null=True, blank=True)
    opp_pts_pg = models.FloatField(null=True, blank=True)
    pts_diff = models.FloatField(null=True, blank=True)

    # Games back
    conference_games_back = models.CharField(max_length=10, blank=True)
    division_games_back = models.CharField(max_length=10, blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["conference", "conference_rank"]
        unique_together = [["team", "season", "season_type"]]

    def __str__(self) -> str:
        return (
            f"{self.team.abbreviation} {self.wins}-{self.losses} "
            f"({self.season} {self.season_type})"
        )


class PlayerSeasonStats(TimestampMixin):
    """Aggregated player season statistics from leaguedashplayerstats."""

    player = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="season_stats",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="player_season_stats",
    )

    # Denormalized for query efficiency
    player_nba_id = models.CharField(max_length=20, db_index=True)
    player_name = models.CharField(max_length=100, blank=True)
    team_abbreviation = models.CharField(max_length=5, blank=True)

    season = models.CharField(max_length=10, db_index=True)
    season_type = models.CharField(max_length=20, db_index=True)
    measure_type = models.CharField(max_length=20, db_index=True)  # Base, Advanced, etc.
    per_mode = models.CharField(max_length=30, db_index=True)  # PerGame, Totals, etc.

    age = models.FloatField(null=True, blank=True)

    # Flexible stats storage — columns vary by measure_type
    stats = models.JSONField(default=dict, blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-season", "player_name"]
        unique_together = [
            ["player_nba_id", "season", "season_type", "measure_type", "per_mode"]
        ]

    def __str__(self) -> str:
        return (
            f"{self.player_name} — {self.measure_type} {self.per_mode} "
            f"({self.season} {self.season_type})"
        )


class TeamSeasonStats(TimestampMixin):
    """Aggregated team season statistics from leaguedashteamstats."""

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="season_stats",
    )

    team_nba_id = models.CharField(max_length=20, db_index=True)
    team_name = models.CharField(max_length=100, blank=True)
    team_abbreviation = models.CharField(max_length=5, blank=True)

    season = models.CharField(max_length=10, db_index=True)
    season_type = models.CharField(max_length=20, db_index=True)
    measure_type = models.CharField(max_length=20, db_index=True)
    per_mode = models.CharField(max_length=30, db_index=True)

    # Flexible stats storage
    stats = models.JSONField(default=dict, blank=True)

    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-season", "team_name"]
        unique_together = [
            ["team_nba_id", "season", "season_type", "measure_type", "per_mode"]
        ]

    def __str__(self) -> str:
        return (
            f"{self.team_name} — {self.measure_type} {self.per_mode} "
            f"({self.season} {self.season_type})"
        )
