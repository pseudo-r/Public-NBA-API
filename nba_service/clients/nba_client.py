"""NBA Stats API client.

Wraps https://stats.nba.com/stats/* using httpx + tenacity retry logic.
All requests automatically include the required NBA WAF headers:
  - Referer: https://www.nba.com/
  - Origin: https://www.nba.com
  - x-nba-stats-origin: stats
  - x-nba-stats-token: true

Usage:
    client = get_nba_client()
    data = client.get_scoreboard("2025-03-25").data
    result_sets = data["resultSets"]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx
import structlog
from django.conf import settings
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = structlog.get_logger(__name__)


@dataclass
class NBAResponse:
    """Parsed response from the NBA Stats API."""

    data: dict[str, Any]
    status_code: int

    def result_set(self, index: int = 0) -> list[dict[str, Any]]:
        """Convert resultSets[index] to a list of dicts keyed by header name."""
        result_sets = self.data.get("resultSets") or []
        if index >= len(result_sets):
            return []
        rs = result_sets[index]
        headers = rs.get("headers", [])
        rows = rs.get("rowSet", [])
        return [dict(zip(headers, row)) for row in rows]

    def named_result_set(self, name: str) -> list[dict[str, Any]]:
        """Find a resultSet by name and convert to list of dicts."""
        result_sets = self.data.get("resultSets") or []
        for rs in result_sets:
            if rs.get("name") == name:
                headers = rs.get("headers", [])
                rows = rs.get("rowSet", [])
                return [dict(zip(headers, row)) for row in rows]
        return []

    def all_result_sets(self) -> dict[str, list[dict[str, Any]]]:
        """Return all resultSets as a name → list[dict] mapping."""
        result_sets = self.data.get("resultSets") or []
        return {
            rs["name"]: [dict(zip(rs["headers"], row)) for row in rs.get("rowSet", [])]
            for rs in result_sets
            if "name" in rs and "headers" in rs
        }

    @property
    def single_result_set(self) -> list[dict[str, Any]]:
        """For leagueleaders-style endpoints that use 'resultSet' (singular)."""
        rs = self.data.get("resultSet") or {}
        headers = rs.get("headers", [])
        rows = rs.get("rowSet", [])
        return [dict(zip(headers, row)) for row in rows]


class NBAClientError(Exception):
    """Raised when the NBA Stats API returns an error."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class NBAClient:
    """HTTP client for stats.nba.com.

    All requests include the required headers to pass the NBA WAF.
    Uses tenacity for automatic retry with exponential backoff.
    """

    def __init__(
        self,
        base_url: str,
        referer: str,
        origin: str,
        origin_header: str,
        token_header: str,
        user_agent: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_backoff: float = 2.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

        self._headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "stats.nba.com",
            "Origin": origin,
            "Referer": referer,
            "User-Agent": user_agent,
            "x-nba-stats-origin": origin_header,
            "x-nba-stats-token": token_header,
        }

        self._client = httpx.Client(
            headers=self._headers,
            timeout=timeout,
            follow_redirects=True,
        )

    # ------------------------------------------------------------------
    # Core request method with retry
    # ------------------------------------------------------------------

    def _make_retry(self) -> Any:
        """Build tenacity retry decorator dynamically from instance config."""
        return retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=self.retry_backoff, min=1, max=30),
            retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
            reraise=True,
        )

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> NBAResponse:
        """Make a GET request to stats.nba.com with automatic retries."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        log = logger.bind(endpoint=endpoint, params=params)

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=self.retry_backoff, min=1, max=30),
            retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
            reraise=True,
        )
        def _do_request() -> NBAResponse:
            try:
                response = self._client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                log.info("nba_api_request_success", status_code=response.status_code)
                return NBAResponse(data=data, status_code=response.status_code)
            except httpx.HTTPStatusError as e:
                log.error(
                    "nba_api_http_error",
                    status_code=e.response.status_code,
                    url=str(e.request.url),
                )
                raise NBAClientError(
                    f"NBA Stats API responded with {e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e
            except httpx.TimeoutException as e:
                log.warning("nba_api_timeout", url=url)
                raise e
            except httpx.ConnectError as e:
                log.error("nba_api_connect_error", url=url)
                raise e

        return _do_request()

    # ------------------------------------------------------------------
    # Game / Scoreboard endpoints
    # ------------------------------------------------------------------

    def get_scoreboard(self, game_date: str) -> NBAResponse:
        """Daily scoreboard.

        Args:
            game_date: Date string in YYYY-MM-DD format.

        Returns:
            NBAResponse with resultSets: GameHeader, LineScore, SeriesStandings,
            LastMeeting, EastConfStandingsByDay, WestConfStandingsByDay,
            Available, TeamLeaders, TicketLinks, WinProbability.
        """
        return self.get(
            "scoreboardv2",
            params={
                "GameDate": game_date,
                "LeagueID": "00",
                "DayOffset": "0",
            },
        )

    def get_boxscore(self, game_id: str) -> NBAResponse:
        """Traditional player and team box score for a completed game.

        Args:
            game_id: 10-digit NBA game ID (e.g., '0022401063').
        """
        return self.get(
            "boxscoretraditionalv2",
            params={
                "GameID": game_id,
                "StartPeriod": "0",
                "EndPeriod": "14",
                "StartRange": "0",
                "EndRange": "28800",
                "RangeType": "0",
            },
        )

    def get_play_by_play(self, game_id: str) -> NBAResponse:
        """Full play-by-play event log for a game.

        Args:
            game_id: 10-digit NBA game ID.
        """
        return self.get(
            "playbyplayv2",
            params={
                "GameID": game_id,
                "StartPeriod": "1",
                "EndPeriod": "4",
            },
        )

    def get_game_summary(self, game_id: str) -> NBAResponse:
        """Game summary: officials, inactive players, arena, attendance."""
        return self.get(
            "boxscoresummaryv2",
            params={"GameID": game_id},
        )

    def get_win_probability(self, game_id: str) -> NBAResponse:
        """Second-by-second win probability for a completed game."""
        return self.get(
            "winprobabilitypbp",
            params={"GameID": game_id, "RunType": "each second"},
        )

    def get_game_rotation(self, game_id: str) -> NBAResponse:
        """Substitution lineup rotation for a game (who was on court, when)."""
        return self.get(
            "gamerotation",
            params={"GameID": game_id, "LeagueID": "00"},
        )

    # ------------------------------------------------------------------
    # Player endpoints
    # ------------------------------------------------------------------

    def get_all_players(self, season: str, is_only_current: bool = True) -> NBAResponse:
        """All registered NBA players (active or historical).

        Args:
            season: Season string, e.g. '2024-25'.
            is_only_current: If True, returns only active players.
        """
        return self.get(
            "commonallplayers",
            params={
                "LeagueID": "00",
                "Season": season,
                "IsOnlyCurrentSeason": "1" if is_only_current else "0",
            },
        )

    def get_player_info(self, player_id: int) -> NBAResponse:
        """Player biography, current team, draft info, headline stats."""
        return self.get(
            "commonplayerinfo",
            params={"PlayerID": str(player_id), "LeagueID": "00"},
        )

    def get_player_career_stats(
        self, player_id: int, per_mode: str = "PerGame"
    ) -> NBAResponse:
        """Season-by-season and career totals for a player.

        Args:
            player_id: NBA player ID.
            per_mode: 'PerGame', 'Totals', 'Per36', 'Per100Possessions', etc.
        """
        return self.get(
            "playercareerstats",
            params={
                "PlayerID": str(player_id),
                "PerMode": per_mode,
                "LeagueID": "00",
            },
        )

    def get_player_game_log(
        self,
        player_id: int,
        season: str,
        season_type: str = "Regular Season",
    ) -> NBAResponse:
        """Game-by-game stats for a player.

        Args:
            player_id: NBA player ID.
            season: Season string, e.g. '2024-25'.
            season_type: 'Regular Season', 'Playoffs', 'Pre Season'.
        """
        return self.get(
            "playergamelog",
            params={
                "PlayerID": str(player_id),
                "Season": season,
                "SeasonType": season_type,
                "LeagueID": "00",
            },
        )

    def get_player_dashboard_splits(
        self,
        player_id: int,
        season: str,
        season_type: str = "Regular Season",
        measure_type: str = "Base",
        per_mode: str = "PerGame",
    ) -> NBAResponse:
        """General splits (home/away, win/loss, month, etc.) for a player."""
        return self.get(
            "playerdashboardbygeneralsplits",
            params={
                "PlayerID": str(player_id),
                "Season": season,
                "SeasonType": season_type,
                "MeasureType": measure_type,
                "PerMode": per_mode,
                "PlusMinus": "N",
                "PaceAdjust": "N",
                "Rank": "N",
                "LeagueID": "00",
                "LastNGames": "0",
                "Month": "0",
                "OpponentTeamID": "0",
                "DateFrom": "",
                "DateTo": "",
                "GameSegment": "",
                "Location": "",
                "Outcome": "",
                "SeasonSegment": "",
                "VsConference": "",
                "VsDivision": "",
                "ShotClockRange": "",
            },
        )

    def get_player_awards(self, player_id: int) -> NBAResponse:
        """All NBA awards won by a player."""
        return self.get(
            "playerawards",
            params={"PlayerID": str(player_id)},
        )

    def get_shot_chart(
        self,
        player_id: int,
        season: str,
        season_type: str = "Regular Season",
        game_id: str = "",
        team_id: int = 0,
    ) -> NBAResponse:
        """Shot chart detail with (x,y) coordinates and shot result.

        Args:
            player_id: NBA player ID.
            season: Season string, e.g. '2024-25'.
            season_type: 'Regular Season' or 'Playoffs'.
            game_id: Optional — filter to a specific game.
            team_id: Optional — filter to a specific team stint.
        """
        return self.get(
            "shotchartdetail",
            params={
                "PlayerID": str(player_id),
                "Season": season,
                "SeasonType": season_type,
                "TeamID": str(team_id),
                "GameID": game_id,
                "LeagueID": "00",
                "ContextMeasure": "FGA",
                "DateFrom": "",
                "DateTo": "",
                "GameSegment": "",
                "LastNGames": "0",
                "Location": "",
                "Month": "0",
                "OpponentTeamID": "0",
                "Outcome": "",
                "Period": "0",
                "RookieYear": "",
                "SeasonSegment": "",
                "VsConference": "",
                "VsDivision": "",
            },
        )

    # ------------------------------------------------------------------
    # Team endpoints
    # ------------------------------------------------------------------

    def get_team_roster(self, team_id: int, season: str) -> NBAResponse:
        """Current roster and coaching staff for a team.

        Args:
            team_id: NBA team ID (10-digit).
            season: Season string, e.g. '2024-25'.
        """
        return self.get(
            "commonteamroster",
            params={
                "TeamID": str(team_id),
                "Season": season,
                "LeagueID": "00",
            },
        )

    def get_team_game_log(
        self,
        team_id: int,
        season: str,
        season_type: str = "Regular Season",
    ) -> NBAResponse:
        """Game-by-game results for a team."""
        return self.get(
            "teamgamelog",
            params={
                "TeamID": str(team_id),
                "Season": season,
                "SeasonType": season_type,
                "LeagueID": "00",
            },
        )

    def get_team_details(self, team_id: int) -> NBAResponse:
        """Team profile: arena, ownership, championships, retired jerseys, Hall of Famers."""
        return self.get(
            "teamdetails",
            params={"TeamID": str(team_id)},
        )

    def get_team_list(self) -> NBAResponse:
        """All team IDs and active year ranges."""
        return self.get(
            "commonteamyears",
            params={"LeagueID": "00"},
        )

    # ------------------------------------------------------------------
    # League / standings / stats
    # ------------------------------------------------------------------

    def get_standings(
        self,
        season: str,
        season_type: str = "Regular Season",
    ) -> NBAResponse:
        """Full conference and division standings.

        Args:
            season: Season string, e.g. '2024-25'.
            season_type: 'Regular Season' or 'Playoffs'.
        """
        return self.get(
            "leaguestandingsv3",
            params={
                "LeagueID": "00",
                "Season": season,
                "SeasonType": season_type,
            },
        )

    def get_league_leaders(
        self,
        season: str,
        season_type: str = "Regular Season",
        stat_category: str = "PTS",
        per_mode: str = "PerGame",
        scope: str = "S",
    ) -> NBAResponse:
        """Ranked stat leaders for a category.

        Note: Response uses 'resultSet' (singular), not 'resultSets'.
        Access via NBAResponse.single_result_set.
        """
        return self.get(
            "leagueleaders",
            params={
                "LeagueID": "00",
                "Season": season,
                "SeasonType": season_type,
                "StatCategory": stat_category,
                "PerMode": per_mode,
                "Scope": scope,
            },
        )

    def get_league_player_stats(
        self,
        season: str,
        season_type: str = "Regular Season",
        measure_type: str = "Base",
        per_mode: str = "PerGame",
        team_id: int = 0,
        last_n_games: int = 0,
    ) -> NBAResponse:
        """Aggregated stats for all players.

        Args:
            season: Season string, e.g. '2024-25'.
            season_type: 'Regular Season', 'Playoffs', etc.
            measure_type: 'Base', 'Advanced', 'Misc', 'Four Factors', 'Scoring',
                          'Opponent', 'Usage', 'Defense'.
            per_mode: 'PerGame', 'Totals', 'Per100Possessions', 'Per36', etc.
            team_id: Filter to a specific team (0 = all).
            last_n_games: Limit to last N games (0 = all).
        """
        return self.get(
            "leaguedashplayerstats",
            params={
                "Season": season,
                "SeasonType": season_type,
                "MeasureType": measure_type,
                "PerMode": per_mode,
                "PlusMinus": "N",
                "PaceAdjust": "N",
                "Rank": "N",
                "LeagueID": "00",
                "LastNGames": str(last_n_games),
                "Month": "0",
                "OpponentTeamID": "0",
                "TeamID": str(team_id),
                "DateFrom": "",
                "DateTo": "",
                "Location": "",
                "Outcome": "",
                "SeasonSegment": "",
                "VsConference": "",
                "VsDivision": "",
                "GameScope": "",
                "GameSegment": "",
                "PlayerExperience": "",
                "PlayerPosition": "",
                "StarterBench": "",
                "College": "",
                "Country": "",
                "DraftPick": "",
                "DraftYear": "",
                "Height": "",
                "Weight": "",
            },
        )

    def get_league_team_stats(
        self,
        season: str,
        season_type: str = "Regular Season",
        measure_type: str = "Base",
        per_mode: str = "PerGame",
        last_n_games: int = 0,
    ) -> NBAResponse:
        """Aggregated stats for all teams."""
        return self.get(
            "leaguedashteamstats",
            params={
                "Season": season,
                "SeasonType": season_type,
                "MeasureType": measure_type,
                "PerMode": per_mode,
                "PlusMinus": "N",
                "PaceAdjust": "N",
                "Rank": "N",
                "LeagueID": "00",
                "LastNGames": str(last_n_games),
                "Month": "0",
                "OpponentTeamID": "0",
                "TeamID": "0",
                "DateFrom": "",
                "DateTo": "",
                "Location": "",
                "Outcome": "",
                "SeasonSegment": "",
                "VsConference": "",
                "VsDivision": "",
                "GameScope": "",
                "GameSegment": "",
            },
        )

    def get_league_game_finder(
        self,
        season: str,
        season_type: str = "Regular Season",
        team_id: int = 0,
        date_from: str = "",
        date_to: str = "",
    ) -> NBAResponse:
        """Search for games by date range or team."""
        return self.get(
            "leaguegamefinder",
            params={
                "PlayerOrTeam": "T",
                "Season": season,
                "SeasonType": season_type,
                "LeagueID": "00",
                "TeamID": str(team_id) if team_id else "",
                "DateFrom": date_from,
                "DateTo": date_to,
            },
        )

    def get_draft_history(self, season: str = "") -> NBAResponse:
        """Full NBA draft history. Pass season='' for all-time."""
        params: dict[str, Any] = {"LeagueID": "00"}
        if season:
            params["Season"] = season
        return self.get("drafthistory", params=params)

    def get_franchise_history(self) -> NBAResponse:
        """Win/loss, playoff appearances, and titles for all franchises (active + defunct)."""
        return self.get("franchisehistory", params={"LeagueID": "00"})

    def get_hustle_stats_player(
        self, season: str, season_type: str = "Regular Season", per_mode: str = "PerGame"
    ) -> NBAResponse:
        """Player-level hustle metrics (deflections, contested shots, charges, box-outs)."""
        return self.get(
            "leaguehustlestatsplayer",
            params={
                "Season": season,
                "SeasonType": season_type,
                "PerMode": per_mode,
                "LeagueID": "00",
                "TeamID": "0",
                "OpponentTeamID": "0",
                "LastNGames": "0",
                "Month": "0",
                "Period": "0",
                "DateFrom": "",
                "DateTo": "",
                "Location": "",
                "Outcome": "",
                "SeasonSegment": "",
                "DraftPick": "",
                "DraftYear": "",
                "GameScope": "",
                "GameSegment": "",
                "PlayerExperience": "",
                "PlayerPosition": "",
                "StarterBench": "",
                "VsConference": "",
                "VsDivision": "",
                "PORound": "",
                "College": "",
                "Country": "",
                "Height": "",
                "Weight": "",
            },
        )

    def get_player_tracking_stats(
        self,
        season: str,
        season_type: str = "Regular Season",
        pt_measure_type: str = "SpeedDistance",
        per_mode: str = "PerGame",
        player_or_team: str = "Player",
    ) -> NBAResponse:
        """Optical tracking stats.

        Args:
            pt_measure_type: One of 'SpeedDistance', 'Possessions', 'CatchShoot',
                'PullUpShot', 'Defense', 'Drives', 'Passing', 'ElbowTouch',
                'PostTouch', 'PaintTouch', 'Efficiency'.
            player_or_team: 'Player' or 'Team'.
        """
        return self.get(
            "leaguedashptstats",
            params={
                "Season": season,
                "SeasonType": season_type,
                "PtMeasureType": pt_measure_type,
                "PerMode": per_mode,
                "PlayerOrTeam": player_or_team,
                "LeagueID": "00",
                "TeamID": "0",
                "OpponentTeamID": "0",
                "LastNGames": "0",
                "Month": "0",
                "Period": "0",
                "Location": "",
                "Outcome": "",
                "SeasonSegment": "",
                "DraftPick": "",
                "DraftYear": "",
                "GameScope": "",
                "GameSegment": "",
                "Height": "",
                "Weight": "",
                "PlayerExperience": "",
                "PlayerPosition": "",
                "StarterBench": "",
                "College": "",
                "Country": "",
                "VsConference": "",
                "VsDivision": "",
                "PORound": "",
                "DateFrom": "",
                "DateTo": "",
            },
        )

    def close(self) -> None:
        """Close the underlying httpx client."""
        self._client.close()

    def __enter__(self) -> "NBAClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


_client_instance: NBAClient | None = None


def get_nba_client() -> NBAClient:
    """Return a singleton NBAClient configured from Django settings."""
    global _client_instance
    if _client_instance is None:
        cfg = settings.NBA_CLIENT
        _client_instance = NBAClient(
            base_url=cfg["BASE_URL"],
            referer=cfg["REFERER"],
            origin=cfg["ORIGIN"],
            origin_header=cfg["ORIGIN_HEADER"],
            token_header=cfg["TOKEN_HEADER"],
            user_agent=cfg["USER_AGENT"],
            timeout=cfg["TIMEOUT"],
            max_retries=cfg["MAX_RETRIES"],
            retry_backoff=cfg["RETRY_BACKOFF"],
        )
    return _client_instance
