# Player Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## Common Player Info

**VERIFIED** — Player biography, current team, position, height/weight, draft info, and headline stats.

**Endpoint:** `GET /commonplayerinfo`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | NBA player ID | `2544` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/commonplayerinfo?PlayerID=2544&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Key Columns |
|------|-------------|
| `CommonPlayerInfo` | `PLAYER_ID`, `FIRST_NAME`, `LAST_NAME`, `BIRTHDATE`, `SCHOOL`, `COUNTRY`, `HEIGHT`, `WEIGHT`, `SEASON_EXP`, `JERSEY`, `POSITION`, `ROSTERSTATUS`, `TEAM_ID`, `TEAM_NAME`, `TEAM_ABBREVIATION`, `DRAFT_YEAR`, `DRAFT_ROUND`, `DRAFT_NUMBER` |
| `PlayerHeadlineStats` | `PLAYER_ID`, `PLAYER_NAME`, `TimeFrame`, `PTS`, `AST`, `REB`, `PIE` |
| `AvailableSeasons` | `SEASON_ID` (all seasons this player has data) |

---

## Player Career Stats

**VERIFIED** — Season-by-season and career totals for a player.

**Endpoint:** `GET /playercareerstats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | NBA player ID | `2544` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per36` | `PerGame` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/playercareerstats?PlayerID=2544&PerMode=PerGame&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Description |
|------|-------------|
| `SeasonTotalsRegularSeason` | Per-season regular season stats |
| `CareerTotalsRegularSeason` | Career totals across all regular seasons |
| `SeasonTotalsPostSeason` | Per-season playoff stats |
| `CareerTotalsPostSeason` | Career playoff totals |
| `SeasonTotalsAllStarSeason` | All-Star game stats (if applicable) |
| `SeasonHighs` | Season-high single-game records per season |
| `CareerHighs` | Career-high single-game records |
| `NextGame` | Upcoming game info |

**Sample row (`SeasonTotalsRegularSeason`):**
```json
["2003-04", "02", "00", "1610612751", "NJN", 62, 2655, 882.0, 1492.0, 20.9, ...]
```
> Columns: `SEASON_ID`, `LEAGUE_ID`, …, `TEAM_ABBREVIATION`, `GP`, `MIN`, `FGM`, `FGA`, `PTS`, etc.

---

## Player Game Log

**VERIFIED** — Game-by-game stats for a player for a specific season.

**Endpoint:** `GET /playergamelog`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | NBA player ID | `2544` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season`, `Playoffs`, `Pre Season` | `Regular Season` |
| `LeagueID` | ✅ | `00` | `00` |
| `DateFrom` | ❌ | Filter start date `MM/DD/YYYY` | `03/01/2025` |
| `DateTo` | ❌ | Filter end date `MM/DD/YYYY` | `03/31/2025` |

```bash
curl "https://stats.nba.com/stats/playergamelog?PlayerID=2544&Season=2024-25&SeasonType=Regular+Season&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`PlayerGameLog` resultSet headers:** `SEASON_ID`, `Player_ID`, `Game_ID`, `GAME_DATE`, `MATCHUP`, `WL`, `MIN`, `FGM`, `FGA`, `FG_PCT`, `FG3M`, `FG3A`, `FG3_PCT`, `FTM`, `FTA`, `FT_PCT`, `OREB`, `DREB`, `REB`, `AST`, `STL`, `BLK`, `TOV`, `PF`, `PTS`, `PLUS_MINUS`, `NBA_FANTASY_PTS`, `VIDEO_AVAILABLE`

---

## Player Dashboard by Year Over Year

**VERIFIED** — Yearly splits for a player (home/away, opponent, win/loss, etc.).

**Endpoint:** `GET /playerdashboardbyyearoveryear`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | NBA player ID | `2544` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season` or `Playoffs` | `Regular Season` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per36` | `PerGame` |
| `MeasureType` | ✅ | `Base`, `Advanced`, `Usage`, `Misc`, `Scoring`, `Defense` | `Base` |
| `PlusMinus` | ❌ | `Y` / `N` | `N` |
| `PaceAdjust` | ❌ | `Y` / `N` | `N` |
| `Rank` | ❌ | `Y` / `N` | `N` |
| `LastNGames` | ❌ | Last N games filter (`0` = all) | `0` |
| `Month` | ❌ | Month number (`0` = all) | `0` |
| `OpponentTeamID` | ❌ | Filter by opponent team | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |

```bash
curl "https://stats.nba.com/stats/playerdashboardbyyearoveryear?PlayerID=2544&Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&MeasureType=Advanced&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:** `OverallPlayerDashboard`, `ByYearPlayerDashboard`

---

## Player Dashboard by General Splits

**VERIFIED** — Splits by location, outcome, clutch, opponent conference, etc.

**Endpoint:** `GET /playerdashboardbygeneralsplits`

Same parameters as `playerdashboardbyyearoveryear`.

**Response `resultSets`:** `OverallPlayerDashboard`, `LocationPlayerDashboard`, `WinsLossesPlayerDashboard`, `MonthPlayerDashboard`, `PrePostAllStarPlayerDashboard`, `StartingPosition`, `DaysRestPlayerDashboard`

---

## Player vs. Player

**VERIFIED** — Head-to-head stats between two specific players.

**Endpoint:** `GET /playervsplayer`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | Primary player ID | `2544` |
| `VsPlayerID` | ✅ | Opponent player ID | `201939` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `PerGame` |
| `MeasureType` | ✅ | `Base`, `Advanced` | `Base` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/playervsplayer?PlayerID=2544&VsPlayerID=201939&Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&MeasureType=Base&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&Location=&Outcome=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:** `Overall`, `onCourt`, `off Court`, `shotChartLeagueAverage`

---

## Shot Chart Detail

**VERIFIED** — Every shot attempt with court coordinates, shot type, result, and zone.

**Endpoint:** `GET /shotchartdetail`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | Player ID (`0` for team) | `2544` |
| `TeamID` | ✅ | Team ID (`0` for all) | `0` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `LeagueID` | ✅ | `00` | `00` |
| `ContextMeasure` | ✅ | `FGA`, `FGM`, `FG3A`, `FG3M`, `FTA`, `BLKA`, `PF`, `PFD` | `FGA` |
| `GameID` | ❌ | Specific game (`""` for all) | `` |
| `DateFrom` | ❌ | Filter start date | `` |
| `DateTo` | ❌ | Filter end date | `` |
| `Period` | ❌ | Quarter (`0` = all) | `0` |
| `LastNGames` | ❌ | Last N games | `0` |
| `Month` | ❌ | Month filter | `0` |
| `OpponentTeamID` | ❌ | Opponent team filter | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `VsConference` | ❌ | `East` or `West` | `` |
| `VsDivision` | ❌ | Division name | `` |
| `AheadBehind` | ❌ | `Ahead or Behind`, `Ahead or Tied`, `Behind or Tied` | `` |
| `ClutchTime` | ❌ | `Last 5 Minutes`, `Last 3 Minutes`, etc. | `` |
| `PointDiff` | ❌ | Point differential filter | `` |

```bash
curl "https://stats.nba.com/stats/shotchartdetail?PlayerID=2544&TeamID=0&Season=2024-25&SeasonType=Regular+Season&LeagueID=00&ContextMeasure=FGA&GameID=&Period=0&LastNGames=0&Month=0&OpponentTeamID=0&Location=&Outcome=&DateFrom=&DateTo=&VsConference=&VsDivision=&AheadBehind=&ClutchTime=&ContextFilter=&RookieYear=&Position=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`Shot_Chart_Detail` resultSet headers (key columns):** `GRID_TYPE`, `GAME_ID`, `GAME_EVENT_ID`, `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `TEAM_NAME`, `PERIOD`, `MINUTES_REMAINING`, `SECONDS_REMAINING`, `EVENT_TYPE`, `ACTION_TYPE`, `SHOT_TYPE`, `SHOT_ZONE_BASIC`, `SHOT_ZONE_AREA`, `SHOT_ZONE_RANGE`, `SHOT_DISTANCE`, `LOC_X`, `LOC_Y`, `SHOT_ATTEMPTED_FLAG`, `SHOT_MADE_FLAG`

**Sample row:**
```json
["Hex Grid", "0022401001", 12, 2544, "LeBron James", 1610612747, "Los Angeles Lakers", 1, 10, 48, "Missed Shot", "Jump Shot", "2PT Field Goal", "Mid-Range", "Right Side Center(RC)", "16-24 ft.", 23, 81, -56, 1, 0]
```

> **Coordinate system:** Center of basket is `(0, 0)`. X is left–right (negative = left, positive = right). Y increases toward half-court. One unit ≈ 1/10 foot.

---

## Player Estimated Metrics

**VERIFIED** — Estimated advanced metrics (based on tracking + stats).

**Endpoint:** `GET /playerestimatedmetrics`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/playerestimatedmetrics?Season=2024-25&SeasonType=Regular+Season&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Key headers:** `PLAYER_ID`, `PLAYER_NAME`, `GP`, `W`, `L`, `MIN`, `E_OFF_RATING`, `E_DEF_RATING`, `E_NET_RATING`, `E_AST_RATIO`, `E_OREB_PCT`, `E_DREB_PCT`, `E_REB_PCT`, `E_TOV_PCT`, `E_USG_PCT`, `E_PACE`, `E_FG_PCT`
