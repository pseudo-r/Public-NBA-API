# Team Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## Common Team Roster

**VERIFIED** — Active roster and coaching staff for a team.

**Endpoint:** `GET /commonteamroster`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | 10-digit team ID | `1610612747` |
| `Season` | ✅ | Season string | `2024-25` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/commonteamroster?TeamID=1610612747&Season=2024-25&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:**

| Name | Key Columns |
|------|-------------|
| `CommonTeamRoster` | `TeamID`, `SEASON`, `LeagueID`, `PLAYER`, `NICKNAME`, `PLAYER_SLUG`, `NUM`, `POSITION`, `HEIGHT`, `WEIGHT`, `BIRTH_DATE`, `AGE`, `EXP`, `SCHOOL`, `PLAYER_ID` |
| `Coaches` | `TEAM_ID`, `SEASON`, `COACH_ID`, `FIRST_NAME`, `LAST_NAME`, `COACH_CODE`, `IS_ASSISTANT`, `COACH_TYPE` |

---

## Team Game Log

**VERIFIED** — Game-by-game results for a team across a season.

**Endpoint:** `GET /teamgamelog`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | 10-digit team ID | `1610612747` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season`, `Playoffs`, `Pre Season` | `Regular Season` |
| `LeagueID` | ✅ | `00` | `00` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |

```bash
curl "https://stats.nba.com/stats/teamgamelog?TeamID=1610612747&Season=2024-25&SeasonType=Regular+Season&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`TeamGameLog` headers:** `Team_ID`, `Game_ID`, `GAME_DATE`, `MATCHUP`, `WL`, `W`, `L`, `W_PCT`, `MIN`, `FGM`, `FGA`, `FG_PCT`, `FG3M`, `FG3A`, `FG3_PCT`, `FTM`, `FTA`, `FT_PCT`, `OREB`, `DREB`, `REB`, `AST`, `STL`, `BLK`, `TOV`, `PF`, `PTS`

---

## Team Dashboard by General Splits

**VERIFIED** — Team season stats with splits (home/away, win/loss, clutch, etc.).

**Endpoint:** `GET /teamdashboardbygeneralsplits`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | 10-digit team ID | `1610612747` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `MeasureType` | ✅ | `Base`, `Advanced`, `Misc`, `Four Factors`, `Scoring`, `Usage`, `Defense`, `Opponent` | `Base` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per100Possessions`, `Per48` | `PerGame` |
| `PlusMinus` | ❌ | `Y` / `N` | `N` |
| `PaceAdjust` | ❌ | `Y` / `N` | `N` |
| `Rank` | ❌ | `Y` / `N` | `N` |
| `LastNGames` | ❌ | `0` = all | `0` |
| `Month` | ❌ | Month number | `0` |
| `OpponentTeamID` | ❌ | Opponent filter | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |
| `VsConference` | ❌ | `East` or `West` | `` |
| `VsDivision` | ❌ | Division name | `` |

```bash
curl "https://stats.nba.com/stats/teamdashboardbygeneralsplits?TeamID=1610612747&Season=2024-25&SeasonType=Regular+Season&MeasureType=Advanced&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response `resultSets`:** `OverallTeamDashboard`, `LocationTeamDashboard`, `WinsLossesTeamDashboard`, `MonthTeamDashboard`, `PrePostAllStarTeamDashboard`, `DaysRestTeamDashboard`

**Advanced measure headers include:** `OFF_RATING`, `DEF_RATING`, `NET_RATING`, `AST_PCT`, `AST_TOV`, `AST_RATIO`, `OREB_PCT`, `DREB_PCT`, `REB_PCT`, `TM_TOV_PCT`, `EFG_PCT`, `TS_PCT`, `PACE`, `PIE`

---

## Team Year-Over-Year

**VERIFIED** — Annual team performance trends across multiple seasons.

**Endpoint:** `GET /teamdashboardbyyearoveryear`

Same parameters as `teamdashboardbygeneralsplits`.

```bash
curl "https://stats.nba.com/stats/teamdashboardbyyearoveryear?TeamID=1610612747&Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Team vs. Player

**VERIFIED** — How a team (or team's players) performed against a specific player.

**Endpoint:** `GET /teamvsplayer`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | Team ID | `1610612747` |
| `VsPlayerID` | ✅ | Opponent player ID | `203999` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `PerGame` |
| `MeasureType` | ✅ | `Base` | `Base` |
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/teamvsplayer?TeamID=1610612747&VsPlayerID=203999&Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&MeasureType=Base&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&Location=&Outcome=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Team Dash Lineups

**VERIFIED** — 2-man, 3-man, 4-man, or 5-man lineup stats for a team (or league-wide).

**Endpoint:** `GET /teamdashlineups`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `TeamID` | ✅ | Team ID (`0` for all teams) | `1610612747` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `MeasureType` | ✅ | `Base`, `Advanced`, `Misc`, `Four Factors`, `Scoring`, `Usage`, `Defense`, `Opponent` | `Advanced` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per100Possessions` | `Per100Possessions` |
| `GroupQuantity` | ✅ | Lineup size: `2`, `3`, `4`, `5` | `5` |
| `PlusMinus` | ❌ | `Y` / `N` | `N` |
| `LastNGames` | ❌ | `0` = all | `0` |
| `Month` | ❌ | Month filter | `0` |
| `OpponentTeamID` | ❌ | Opponent filter | `0` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |

```bash
# Team 5-man lineup advanced stats
curl "https://stats.nba.com/stats/teamdashlineups?TeamID=1610612747&Season=2024-25&SeasonType=Regular+Season&MeasureType=Advanced&PerMode=Per100Possessions&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&GroupQuantity=5&LastNGames=0&Month=0&OpponentTeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Key response columns:** `GROUP_ID`, `GROUP_NAME`, `GP`, `W`, `L`, `W_PCT`, `MIN`, `OFF_RATING`, `DEF_RATING`, `NET_RATING`, `AST_PCT`, `EFG_PCT`, `TS_PCT`, `PACE`, `PIE`, `PLUS_MINUS`

> **Note:** `GROUP_NAME` is a hyphen-separated list of player names in the lineup. `GROUP_ID` contains underscore-separated player IDs.

---

## League Dash Lineups

**VERIFIED** — League-wide lineup stats (every team, every 5-man unit).

**Endpoint:** `GET /leaguedashlineups`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `MeasureType` | ✅ | `Base`, `Advanced`, `Misc`, `Four Factors`, `Scoring`, `Opponent` | `Advanced` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per100Possessions` | `Per100Possessions` |
| `GroupQuantity` | ✅ | `2` through `5` | `5` |
| `LeagueID` | ✅ | `00` | `00` |
| `TeamID` | ❌ | Filter to a team | `0` |
| `DateFrom` | ❌ | Date filter | `` |
| `DateTo` | ❌ | Date filter | `` |
| `LastNGames` | ❌ | Last N games | `0` |
| `Month` | ❌ | Month | `0` |
| `OpponentTeamID` | ❌ | Opponent filter | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |

```bash
curl "https://stats.nba.com/stats/leaguedashlineups?Season=2024-25&SeasonType=Regular+Season&MeasureType=Advanced&PerMode=Per100Possessions&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&GroupQuantity=5&TeamID=0&LastNGames=0&Month=0&OpponentTeamID=0&Location=&Outcome=&DateFrom=&DateTo=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Common All Available Teams

**VERIFIED** — List of all active NBA teams with IDs and abbreviations.

**Endpoint:** `GET /commonteamyears`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |

```bash
curl "https://stats.nba.com/stats/commonteamyears?LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`TeamYears` headers:** `LEAGUE_ID`, `TEAM_ID`, `MIN_YEAR`, `MAX_YEAR`, `ABBREVIATION`
