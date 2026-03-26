# Game Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## Scoreboard v2

**VERIFIED** — Daily scores, tip-off times, arena info, and team linescore.

**Endpoint:** `GET /scoreboardv2`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameDate` | ✅ | Date in `YYYY-MM-DD` | `2025-03-26` |
| `LeagueID` | ✅ | `00` NBA · `10` WNBA · `20` G League | `00` |
| `DayOffset` | ✅ | Days from `GameDate` (always `0`) | `0` |

```bash
curl "https://stats.nba.com/stats/scoreboardv2?GameDate=2025-03-26&LeagueID=00&DayOffset=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Description |
|------|-------------|
| `GameHeader` | Game ID, status text, arena, broadcast, tip-off time |
| `LineScore` | Per-team quarter scores and totals |
| `SeriesStandings` | Playoff series records (empty in regular season) |
| `LastMeeting` | Most recent prior meeting between the two teams |
| `EastConfStandingsbyDay` | East conference standings as of game date |
| `WestConfStandingsbyDay` | West conference standings as of game date |
| `Available` | Which games have full data available |
| `TeamLeaders` | Pts/Reb/Ast leaders for each team |
| `TicketLinks` | Ticket purchase links (may be empty) |
| `WinProbability` | Pre-game win probability if available |

**Sample response (trimmed):**
```json
{
  "resultSets": [
    {
      "name": "GameHeader",
      "headers": ["GAME_DATE_EST","GAME_SEQUENCE","GAME_ID","GAME_STATUS_ID","GAME_STATUS_TEXT","GAMECODE","HOME_TEAM_ID","VISITOR_TEAM_ID","SEASON","LIVE_PERIOD","LIVE_PC_TIME","NATL_TV_BROADCASTER_ABBREVIATION","LIVE_PERIOD_TIME_BCAST","WH_STATUS"],
      "rowSet": [["2025-03-26T00:00:00", 1, "0022401063", 3, "Final", "20250326/CHAPAT", 1610612766, 1610612752, "2024", 0, "PT00M00.00S", "ESPN", "Q4       - ", 1]]
    }
  ]
}
```

---

## Scoreboard v3

**VERIFIED** — Same as v2 but returns a modern JSON object instead of `resultSets`. Preferred for new integrations.

**Endpoint:** `GET /scoreboardv3`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameDate` | ✅ | Date in `YYYY-MM-DD` | `2025-03-26` |
| `LeagueID` | ✅ | `00` NBA | `00` |

```bash
curl "https://stats.nba.com/stats/scoreboardv3?GameDate=2025-03-26&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Sample response (trimmed):**
```json
{
  "scoreboard": {
    "gameDate": "2025-03-26",
    "leagueId": "00",
    "leagueName": "National Basketball Association",
    "games": [
      {
        "gameId": "0022401063",
        "gameCode": "20250326/CHAPAT",
        "gameStatus": 3,
        "gameStatusText": "Final",
        "period": 4,
        "gameClock": "",
        "gameTimeUTC": "2025-03-26T23:00:00Z",
        "homeTeam": { "teamId": 1610612766, "teamCity": "Charlotte", "teamName": "Hornets", "score": 109, "inBonus": "0", "timeoutsRemaining": 0 },
        "awayTeam": { "teamId": 1610612752, "teamCity": "New York", "teamName": "Knicks", "score": 107, "inBonus": "0", "timeoutsRemaining": 0 }
      }
    ]
  }
}
```

> **Note:** `gameStatus` values: `1` = Scheduled · `2` = Live · `3` = Final

---

## Boxscore Traditional v2

**VERIFIED** — Player-level and team-level traditional stats (Pts, Reb, Ast, FG%, etc.) for a game.

**Endpoint:** `GET /boxscoretraditionalv2`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |
| `StartPeriod` | ✅ | Start period (use `0` for full game) | `0` |
| `EndPeriod` | ✅ | End period (use `14` for OT support) | `14` |
| `StartRange` | ✅ | Always `0` | `0` |
| `EndRange` | ✅ | Always `28800` | `28800` |
| `RangeType` | ✅ | Always `0` | `0` |

```bash
curl "https://stats.nba.com/stats/boxscoretraditionalv2?GameID=0022401063&StartPeriod=0&EndPeriod=14&StartRange=0&EndRange=28800&RangeType=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Description |
|------|-------------|
| `PlayerStats` | Per-player stats: MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FTM, FTA, OREB, DREB, REB, AST, STL, BLK, TO, PF, PTS, PLUS_MINUS |
| `TeamStats` | Same columns aggregated at team level |
| `TeamStartersBenchStats` | Starters vs bench split per team |

```python
import requests

headers = {
    "Referer": "https://www.nba.com/",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

url = "https://stats.nba.com/stats/boxscoretraditionalv2"
params = {
    "GameID": "0022401063",
    "StartPeriod": 0, "EndPeriod": 14,
    "StartRange": 0, "EndRange": 28800, "RangeType": 0
}
r = requests.get(url, params=params, headers=headers)
player_stats = r.json()["resultSets"][0]
# player_stats["headers"] → ["GAME_ID","TEAM_ID","TEAM_ABBREVIATION","TEAM_CITY","PLAYER_ID","PLAYER_NAME","NICKNAME","START_POSITION","COMMENT","MIN","FGM","FGA",...]
# player_stats["rowSet"][0] → first player's row
```

---

## Boxscore Advanced v2

**VERIFIED** — Advanced per-game metrics: OffRtg, DefRtg, NetRtg, AST%, REB%, TS%, PACE.

**Endpoint:** `GET /boxscoreadvancedv2`

Same parameters as Boxscore Traditional v2.

```bash
curl "https://stats.nba.com/stats/boxscoreadvancedv2?GameID=0022401063&StartPeriod=0&EndPeriod=14&StartRange=0&EndRange=28800&RangeType=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`PlayerStats` headers include:** `OFF_RATING`, `DEF_RATING`, `NET_RATING`, `AST_PCT`, `AST_TOV`, `AST_RATIO`, `OREB_PCT`, `DREB_PCT`, `REB_PCT`, `TM_TOV_PCT`, `EFG_PCT`, `TS_PCT`, `USG_PCT`, `E_USG_PCT`, `E_PACE`, `PACE`, `PACE_PER40`, `POSS`, `PIE`

---

## Boxscore Other Variants

**PARTIALLY VERIFIED** — Same parameters as traditional v2 unless noted.

| Endpoint | Description |
|----------|-------------|
| `/boxscorescoringv2` | Scoring breakdown by shot type and distance |
| `/boxscoremisc v2` | Misc stats: PTS off TO, FB PTS, 2nd chance PTS |
| `/boxscorefourfactorsv2` | Four factors: EFG%, TOV%, OREB%, FTRate |
| `/boxscoreusagev2` | Usage rate, usage-adjusted stats |
| `/boxscoredefensivev2` | Defensive stats: contested shots, deflections |
| `/boxscorematchupsv3` | Matchup-level data (v3 format, GameID + LeagueID) |
| `/boxscoretraditionalv3` | Traditional stats in v3 object format |
| `/boxscoreadvancedv3` | Advanced stats in v3 object format |

---

## Play-By-Play v2

**VERIFIED** — Full event log for a game: plays, descriptions, scores, and clock.

**Endpoint:** `GET /playbyplayv2`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |
| `StartPeriod` | ✅ | `1` through `10` (OT periods) | `1` |
| `EndPeriod` | ✅ | `1` through `10` | `4` |

```bash
curl "https://stats.nba.com/stats/playbyplayv2?GameID=0022401063&StartPeriod=1&EndPeriod=4" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`PlayByPlay` resultSet headers:** `GAME_ID`, `EVENTNUM`, `EVENTMSGTYPE`, `EVENTMSGACTIONTYPE`, `PERIOD`, `WCTIMESTRING`, `PCTIMESTRING`, `HOMEDESCRIPTION`, `NEUTRALDESCRIPTION`, `VISITORDESCRIPTION`, `SCORE`, `SCOREMARGIN`

**Event message types (`EVENTMSGTYPE`):**

| Value | Event |
|-------|-------|
| `1` | Made shot |
| `2` | Missed shot |
| `3` | Free throw |
| `4` | Rebound |
| `5` | Turnover |
| `6` | Foul |
| `7` | Violation |
| `8` | Substitution |
| `9` | Timeout |
| `10` | Jump ball |
| `11` | Ejection |
| `12` | Start of period |
| `13` | End of period |

---

## Play-By-Play v3

**VERIFIED** — Modern v3 format with richer play data (action numbers, qualifiers, player IDs).

**Endpoint:** `GET /playbyplayv3`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |
| `StartPeriod` | ✅ | Use `0` for all | `0` |
| `EndPeriod` | ✅ | Use `0` for all | `0` |

```bash
curl "https://stats.nba.com/stats/playbyplayv3?GameID=0022401063&StartPeriod=0&EndPeriod=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Sample response:**
```json
{
  "game": {
    "gameId": "0022401063",
    "actions": [
      {
        "actionNumber": 2,
        "clock": "PT12M00.00S",
        "period": 1,
        "teamId": 1610612766,
        "teamTricode": "CHA",
        "personId": 1629640,
        "playerName": "P.J. Washington",
        "actionType": "jumpball",
        "subType": "lost",
        "description": "Jump Ball C. Boucher vs. P.J. Washington: Tip to ...",
        "scoreHome": "0",
        "scoreAway": "0",
        "qualifiers": []
      }
    ]
  }
}
```

---

## Win Probability PBP

**PARTIALLY VERIFIED** — Second-by-second win probability for each team throughout a game.

**Endpoint:** `GET /winprobabilitypbp`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |
| `RunType` | ✅ | `each second` or `each play` | `each second` |

```bash
curl "https://stats.nba.com/stats/winprobabilitypbp?GameID=0022401063&RunType=each+second" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`WinProbPBP` resultSet headers:** `GAME_ID`, `EVENT_NUM`, `HOME_PCT`, `VISITOR_PCT`, `PERIOD`, `SECONDS_REMAINING`, `HOME_PTS`, `VISITOR_PTS`, `LAST_ACTION`

> **Notes:**
> - Only available for completed games
> - May return empty `rowSet` for very old games (pre-2016)
> - `RunType=each+second` returns a large payload — use `each+play` for lighter responses

---

## Game Summary

**VERIFIED** — High-level game summary: officials, inactive players, line scores, and team stats.

**Endpoint:** `GET /boxscoresummaryv2`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |

```bash
curl "https://stats.nba.com/stats/boxscoresummaryv2?GameID=0022401063" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:** `GameSummary`, `OtherStats`, `Officials`, `InactivePlayers`, `GameInfo`, `LineScore`, `LastMeeting`, `SeasonSeries`, `AvailableVideo`
