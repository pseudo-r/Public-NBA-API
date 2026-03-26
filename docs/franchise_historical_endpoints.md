# Franchise & Historical Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## Franchise History

**VERIFIED** — Win/loss records, playoff appearances, and title history for all active and defunct franchises.

**Endpoint:** `GET /franchisehistory`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/franchisehistory?LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Description |
|------|-------------|
| `FranchiseHistory` | Active franchises — all seasons, win/loss, titles |
| `DefunctTeams` | Historical teams no longer in operation |

**Both result sets share headers:** `LEAGUE_ID`, `TEAM_ID`, `TEAM_CITY`, `TEAM_NAME`, `START_YEAR`, `END_YEAR`, `YEARS`, `GAMES`, `WINS`, `LOSSES`, `WIN_PCT`, `PO_APPEARANCES`, `DIV_TITLES`, `CONF_TITLES`, `LEAGUE_TITLES`

---

## Franchise Leaders

**VERIFIED** — All-time statistical leaders for a franchise.

**Endpoint:** `GET /franchiseleaders`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | 10-digit team ID | `1610612747` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/franchiseleaders?TeamID=1610612747&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`FranchiseLeaders` headers:** `TEAM_ID`, `PTS`, `PTS_PERSON_ID`, `PTS_PLAYER`, `AST`, `AST_PERSON_ID`, `AST_PLAYER`, `REB`, `REB_PERSON_ID`, `REB_PLAYER`, `BLK`, `BLK_PERSON_ID`, `BLK_PLAYER`, `STL`, `STL_PERSON_ID`, `STL_PLAYER`

---

## Franchise Players

**PARTIALLY VERIFIED** — All players who have appeared for a franchise.

**Endpoint:** `GET /franchiseplayers`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | 10-digit team ID | `1610612747` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/franchiseplayers?TeamID=1610612747&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`FranchisePlayers` headers:** `TEAM_ID`, `PLAYER_ID`, `PLAYER`, `SEA`, `GP`, `MIN`, `PTS`, `AST`, `REB`

---

## Team Details

**VERIFIED** — Deep team profile: arena, ownership, championships, retired jerseys, Hall of Famers, social links.

**Endpoint:** `GET /teamdetails`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | 10-digit team ID | `1610612739` |

```bash
curl "https://stats.nba.com/stats/teamdetails?TeamID=1610612747" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Key Columns |
|------|-------------|
| `TeamBackground` | `TEAM_ID`, `ABBREVIATION`, `NICKNAME`, `YEARFOUNDED`, `CITY`, `ARENA`, `ARENACAPACITY`, `OWNER`, `GENERALMANAGER`, `HEADCOACH`, `DLEAGUEAFFILIATION` |
| `TeamHistory` | `TEAM_ID`, `CITY`, `NICKNAME`, `YEARFOUNDED`, `YEARACTIVETILL` |
| `TeamAwardsChampionships` | `YEARAWARDED`, `OPPOSITETEAM` |
| `TeamAwardsConf` | `YEARAWARDED`, `OPPOSITETEAM` |
| `TeamAwardsDiv` | `YEARAWARDED`, `OPPOSITETEAM` |
| `TeamHof` | `PLAYERID`, `PLAYER`, `POSITION`, `JERSEY`, `SEASONSWITHTEAM`, `YEAR` |
| `TeamRetired` | `PLAYERID`, `PLAYER`, `POSITION`, `JERSEY`, `SEASONSWITHTEAM`, `YEAR` |
| `TeamSocialSites` | `ACCOUNTTYPE`, `WEBSITE_LINK` |

---

## All-Time Leaders Grids

**VERIFIED** — Career all-time leaders across key stat categories.

**Endpoint:** `GET /alltimeleadersgrids`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `SeasonType` | ✅ | `Regular Season`, `Playoffs`, `Pre Season` | `Regular Season` |
| `TopX` | ✅ | Number of leaders to return per category | `10` |
| `PerMode` | ✅ | `Totals` or `PerGame` | `Totals` |

```bash
curl "https://stats.nba.com/stats/alltimeleadersgrids?LeagueID=00&SeasonType=Regular+Season&TopX=10&PerMode=Totals" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`** — one per stat category: `PtsLeaders`, `AstLeaders`, `RebLeaders`, `BlkLeaders`, `StlLeaders`, `FGMLeaders`, `FGALeaders`, `FG3MLeaders`, `FG3ALeaders`, `FTMLeaders`, `FTALeaders`, `OrRebLeaders`, `DrRebLeaders`, `GpLeaders`, `PFLeaders`, `GamesLeaders`

Each set has headers: `PLAYER_ID`, `PLAYER_NAME`, `[STAT]`, `[STAT]_RANK`

---

## Game Rotation

**VERIFIED** — Full substitution lineup for each team in a game (who was on court, when, and how they performed).

**Endpoint:** `GET /gamerotation`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/gamerotation?GameID=0022401063&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Headers |
|------|---------|
| `HomeTeam` | `GAME_ID`, `TEAM_ID`, `TEAM_CITY`, `TEAM_NAME`, `PERSON_ID`, `PLAYER_FIRST`, `PLAYER_LAST`, `IN_TIME_REAL`, `OUT_TIME_REAL`, `PLAYER_PTS`, `PT_DIFF`, `USG_PCT` |
| `AwayTeam` | Same columns |

> Each row is one player stint on court. `IN_TIME_REAL` and `OUT_TIME_REAL` are in tenths of seconds from game start.

---

## Player Compared

**PARTIALLY VERIFIED** — Side-by-side stats comparison for two players in overlapping games.

**Endpoint:** `GET /playercompare`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerIDList` | ✅ | Comma-separated player IDs | `2544,201939` |
| `VsPlayerIDList` | ✅ | Comma-separated opponent player IDs | `203999,201142` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `MeasureType` | ✅ | Measure type | `Base` |
| `PerMode` | ✅ | Per mode | `PerGame` |
| `LeagueID` | ✅ | `00` | `00` |
| `PlusMinus` | ❌ | `Y` / `N` | `N` |
| `LastNGames` | ❌ | Last N games | `0` |
| `Month` | ❌ | Month | `0` |
| `OpponentTeamID` | ❌ | Opponent | `0` |

```bash
curl "https://stats.nba.com/stats/playercompare?PlayerIDList=2544,201939&VsPlayerIDList=203999,201142&Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&Location=&Outcome=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Player Awards

**VERIFIED** — All NBA awards won by a specific player.

**Endpoint:** `GET /playerawards`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerID` | ✅ | NBA player ID | `2544` |

```bash
curl "https://stats.nba.com/stats/playerawards?PlayerID=2544" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`PlayerAwards` headers:** `PERSON_ID`, `FIRST_NAME`, `LAST_NAME`, `TEAM`, `DESCRIPTION`, `ALL_NBA_TEAM_NUMBER`, `SEASON`, `MONTH`, `WEEK`, `CONFERENCE`, `TYPE`, `SUBTYPE1`, `SUBTYPE2`, `SUBTYPE3`

---

## Common Playoff Series

**PARTIALLY VERIFIED** — All playoff series matchups for a season.

**Endpoint:** `GET /commonplayoffseries`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `Season` | ✅ | Season string | `2023-24` |
| `SeriesID` | ❌ | Filter to specific series | `` |

```bash
curl "https://stats.nba.com/stats/commonplayoffseries?LeagueID=00&Season=2023-24" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`PlayoffSeries` headers:** `GAME_ID`, `HOME_TEAM_ID`, `VISITOR_TEAM_ID`, `SEASON`, `SERIES_ID`, `GAME_NUM`, `HOME_TEAM_WINS`, `HOME_TEAM_LOSSES`, `SERIES_LEADER`
