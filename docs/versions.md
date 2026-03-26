# API Versions: v1 vs v2 vs v3

> **Live-tested** on 2026-03-26 via browser fetch from `nba.com` with correct WAF headers.

The NBA Stats API has three response format generations. The version is indicated by the URL suffix (e.g., `scoreboardv2`, `scoreboardv3`). Unversioned endpoints behave like v2.

---

## At a Glance

| | v1 / unversioned | v2 | v3 |
|---|---|---|---|
| **Examples** | `leaguedashplayerstats`, `commonallplayers`, `leagueleaders` | `scoreboardv2`, `boxscoretraditionalv2`, `playbyplayv2` | `scoreboardv3`, `boxscoretraditionalv3`, `playbyplayv3` |
| **Top-level keys** | `resource`, `parameters`, `resultSets` | `resource`, `parameters`, `resultSets` | `meta`, `<namedObject>` |
| **Data structure** | `resultSets[i].headers` + `rowSet` | Same | Nested JSON objects (camelCase) |
| **Parse method** | `zip(headers, row)` | `zip(headers, row)` | Direct key access |
| **Status** | Stable | Stable | Active (newer endpoints added here) |

---

## v2 Response Format

The legacy format used by the majority of endpoints. Data is encoded as a 2D array (`rowSet`) with a separate `headers` array.

```json
{
  "resource": "scoreboardv2",
  "parameters": { "GameDate": "2025-03-25", "LeagueID": "00", "DayOffset": "0" },
  "resultSets": [
    {
      "name": "GameHeader",
      "headers": ["GAME_DATE_EST", "GAME_SEQUENCE", "GAME_ID", "GAME_STATUS_ID",
                  "GAME_STATUS_TEXT", "GAMECODE", "HOME_TEAM_ID", "VISITOR_TEAM_ID",
                  "SEASON", "LIVE_PERIOD", "LIVE_PC_TIME", "NATL_TV_BROADCASTER_ABBREVIATION",
                  "LIVE_PERIOD_TIME_BCAST", "WH_STATUS"],
      "rowSet": [
        ["2025-03-25T00:00:00", 1, "0022401045", 3, "Final", "20250325/ORLCHA",
         1610612741, 1610612753, "2024", 0, "", "", "Q4", 1]
      ]
    }
  ]
}
```

**Python parse:**
```python
rs = data["resultSets"][0]
rows = [dict(zip(rs["headers"], row)) for row in rs["rowSet"]]
```

---

## v3 Response Format

Modern format. Data is returned as named nested JSON objects using camelCase keys. No `headers`/`rowSet` arrays.

```json
{
  "meta": {
    "version": 1,
    "request": "http://nba.cloud/league/00/2025/03/25/scoreboard?Format=json",
    "time": "2025-07-03T07:11:03.113Z"
  },
  "scoreboard": {
    "gameDate": "2025-03-25",
    "leagueId": "00",
    "leagueName": "National Basketball Association",
    "games": [
      {
        "gameId": "0022401045",
        "gameCode": "20250325/ORLCHA",
        "gameStatus": 3,
        "gameStatusText": "Final",
        "period": 4,
        "gameClock": "",
        "gameTimeUTC": "2025-03-25T23:00:00Z",
        "gameEt": "2025-03-25T19:00:00Z",
        "homeTeam": { "teamId": 1610612741, "teamCity": "Chicago", ... },
        "awayTeam": { "teamId": 1610612753, "teamCity": "Orlando", ... }
      }
    ]
  }
}
```

**Python parse:**
```python
games = data["scoreboard"]["games"]
for game in games:
    print(game["gameId"], game["gameStatusText"])
```

---

## Live Test Results (2026-03-26)

### Scoreboard

| Endpoint | Status | Format | Top-level data key | Key game fields |
|---|---|---|---|---|
| `scoreboardv2` | ✅ 200 | v2 | `resultSets` | `GameHeader`, `LineScore`, `EastConfStandingsByDay`, `WestConfStandingsByDay` |
| `scoreboardv3` | ✅ 200 | v3 | `scoreboard` | `gameDate`, `leagueId`, `leagueName`, `games[]` |

### Boxscore Traditional

| Endpoint | Status | Format | Top-level data key | Key fields |
|---|---|---|---|---|
| `boxscoretraditionalv2` | ✅ 200 | v2 | `resultSets` | `PlayerStats` (GAME_ID, TEAM_ID, PLAYER_ID, PLAYER_NAME, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FTM, FTA, OREB, DREB, REB, AST, STL, BLK, TO, PF, PTS, PLUS_MINUS), `TeamStats`, `TeamStarterBenchStats` |
| `boxscoretraditionalv3` | ✅ 200 | v3 | `boxScoreTraditional` | `gameId`, `awayTeamId`, `homeTeamId`, `homeTeam{teamId, teamCity, teamName, teamTricode, players[{personId, firstName, familyName, nameI, position, jerseyNum, statistics{minutes, fieldGoalsMade, assists, ...}}]}`, `awayTeam{...}` |

> **v3 boxscore key difference:** Player stats are inside `player.statistics{}` as camelCase keys (`fieldGoalsMade` not `FGM`). `minutes` is a string like `"39:36"`.

### Play-By-Play

| Endpoint | Status | Format | Top-level data key | Notes |
|---|---|---|---|---|
| `playbyplayv2` | ✅ 200 | v2 | `resultSets` | Returns `PlayByPlay` result set with `EVENTNUM`, `EVENTMSGTYPE`, `PERIOD`, `PCTIMESTRING`, `HOMEDESCRIPTION`, `VISITORDESCRIPTION`, `SCORE`, `SCOREMARGIN`. **Returns `{}` if GameID has no data.** |
| `playbyplayv3` | ✅ 200 | v3 | `game` | `game.gameId`, `game.videoAvailable`, `game.actions[]` with `actionNumber`, `clock` (ISO 8601 duration e.g. `"PT12M00.00S"`), `period`, `teamId`, `teamTricode`, `personId`, `playerName`, `actionType`, `subType`, `description`, `scoreHome`, `scoreAway`, `qualifiers[]` |

> **v3 clock format:** `"PT12M00.00S"` (ISO 8601 duration) vs v2 `"12:00"` plain string.

### Standings & Stats (v2-style despite naming)

| Endpoint | Status | Format | resultSet name | Key column sample |
|---|---|---|---|---|
| `leaguestandingsv3` | ✅ 200 | **v2 style** ⚠️ | `Standings` | `TEAM_ID`, `CONFERENCE`, `DIVISION`, `WINS`, `LOSSES`, `WinPct`, `ConferenceRank`, `HOME_W`, `HOME_L`, `ROAD_W`, `ROAD_L`, `L10_W`, `L10_L` |
| `commonallplayers` | ✅ 200 | v2 | `CommonAllPlayers` | `PERSON_ID`, `DISPLAY_FIRST_LAST`, `TEAM_ID`, `TEAM_CITY`, `TEAM_NAME`, `TEAM_ABBREVIATION`, `TEAM_CODE`, `TEAM_SLUG`, `GAMES_PLAYED_FLAG`, `OTHERLEAGUE_EXPERIENCE_CH`, `FROM_YEAR`, `TO_YEAR`, `ROSTERSTATUS` |
| `leaguedashplayerstats` | ✅ 200 | v2 | `LeagueDashPlayerStats` | `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `TEAM_ABBREVIATION`, `AGE`, `GP`, `W`, `L`, `W_PCT`, `MIN`, `FGM`, `FGA`, `FG_PCT`, `FG3M`, `FG3A`, `FG3_PCT`, `FTM`, `FTA`, `FT_PCT`, `OREB`, `DREB`, `REB`, `AST`, `TOV`, `STL`, `BLK`, `BLKA`, `PF`, `PFD`, `PTS`, `PLUS_MINUS` |

> ⚠️ `leaguestandingsv3` has `v3` in the URL but returns the legacy `resultSets` format. Don't be fooled by the name.

---

## Which Version Should You Use?

| Use case | Recommendation |
|---|---|
| Daily scoreboard | `scoreboardv3` — richer game object, no parsing needed |
| Box score for display | `boxscoretraditionalv3` — nested, no zip() needed |
| Play-by-play | `playbyplayv3` — richer action data, ISO 8601 clock |
| Standings | `leaguestandingsv3` (v2 format internally) |
| Player/team stats bulk | Unversioned `leaguedashplayerstats` / `leaguedashteamstats` |
| All players list | Unversioned `commonallplayers` |
| Legacy integrations | v2 endpoints — all stable, no plans to deprecate |
