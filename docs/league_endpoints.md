# League Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## League Standings v3

**VERIFIED** — Full conference and division standings with detailed records.

**Endpoint:** `GET /leaguestandingsv3`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` NBA | `00` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season` or `Playoffs` | `Regular Season` |
| `Section` | ❌ | `overall`, `conference`, or `division` | `overall` |

```bash
curl "https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2024-25&SeasonType=Regular+Season&Section=overall" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`Standings` resultSet headers (key columns):** `LeagueID`, `SeasonID`, `TeamID`, `TeamCity`, `TeamName`, `TeamSlug`, `Conference`, `ConferenceRecord`, `PlayoffRank`, `ClinchIndicator`, `Division`, `DivisionRecord`, `DivisionRank`, `WINS`, `LOSSES`, `WinPCT`, `LeagueRank`, `Record`, `HOME`, `ROAD`, `L10`, `Last10Home`, `Last10Road`, `OT`, `ThreePTSOrLess`, `TenPTSOrMore`, `LongHomeStreak`, `LongRoadStreak`, `LongWinStreak`, `LongLossStreak`, `CurrentHomeStreak`, `CurrentRoadStreak`, `CurrentStreak`, `Conference_WINS`, `Conference_LOSSES`, `ConferenceGamesBack`, `ClinchedConferenceTitle`, `ClinchedDivisionTitle`, `ClinchedPlayoffBirth`, `ClinchedPlayIn`, `EliminatedConference`, `Points_PG`, `OppPoints_PG`, `DiffPoints_PG`

**Sample row:**
```json
["00", "22024", 1610612738, "Boston", "Celtics", "celtics", "East", "29-10", 1, "z", "Atlantic", "11-1", 1, 53, 16, 0.768, 1, "53-16", "29-6", "24-10", "7-3", "16-3", "8-7", ...]
```

> **Clinch indicators:** `z` = clinched top seed · `c` = clinched conference · `p` = clinched playoff berth · `x` = clinched division · `pi` = play-in eligible

---

## League Leaders

**VERIFIED** — Ranked stat leaders for a specific category.

**Endpoint:** `GET /leagueleaders`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season`, `Playoffs`, `Pre Season` | `Regular Season` |
| `StatCategory` | ✅ | Stat to rank by | `PTS` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `PerGame` |
| `Scope` | ✅ | `S` (qualified), `RS` (rookies), `SP` (rookies & sophs) | `S` |

**`StatCategory` values:**

| Code | Stat |
|------|------|
| `PTS` | Points |
| `REB` | Rebounds |
| `AST` | Assists |
| `STL` | Steals |
| `BLK` | Blocks |
| `FGM` | Field Goals Made |
| `FGA` | Field Goals Attempted |
| `FG_PCT` | FG Percentage |
| `FG3M` | 3-Pointers Made |
| `FG3A` | 3-Pointers Attempted |
| `FG3_PCT` | 3-Point Percentage |
| `FTM` | Free Throws Made |
| `FTA` | Free Throws Attempted |
| `FT_PCT` | Free Throw Percentage |
| `OREB` | Offensive Rebounds |
| `DREB` | Defensive Rebounds |
| `TOV` | Turnovers |
| `EFF` | Efficiency |
| `MIN` | Minutes |

```bash
# Scoring leaders (per game)
curl "https://stats.nba.com/stats/leagueleaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2024-25&SeasonType=Regular+Season&StatCategory=PTS" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Response** is a single `resultSet` (not `resultSets` array):
```json
{
  "resultSet": {
    "name": "LeagueLeaders",
    "headers": ["PLAYER_ID","PLAYER","TEAM","GP","MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","REB","AST","STL","BLK","TOV","PF","PTS","EFF","AST_TOV","STL_TOV"],
    "rowSet": [[1641705, "Victor Wembanyama", "SAS", 54, 31.1, 9.1, 20.1, 0.45, 2.3, 6.4, 0.36, 5.3, 6.5, 0.82, 1.2, 7.3, 8.5, 3.9, 1.5, 4.4, 2.6, 2.0, 25.9, 26.6, 1.5, 0.6]]
  }
}
```

> **Note:** `leagueleaders` uses `resultSet` (singular) not `resultSets`. Access via `r.json()["resultSet"]`, not `r.json()["resultSets"][0]`.

---

## League Dash Player Stats

**VERIFIED** — Aggregated stats for all players (or filtered) in a season with flexible measure types.

**Endpoint:** `GET /leaguedashplayerstats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `MeasureType` | ✅ | `Base`, `Advanced`, `Misc`, `Four Factors`, `Scoring`, `Usage`, `Defense`, `Opponent` | `Base` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per100Possessions`, `Per36`, `Per48`, `Per40` | `PerGame` |
| `LeagueID` | ✅ | `00` | `00` |
| `PlusMinus` | ❌ | `Y` / `N` | `N` |
| `PaceAdjust` | ❌ | `Y` / `N` | `N` |
| `Rank` | ❌ | `Y` / `N` | `N` |
| `TeamID` | ❌ | Filter to team | `0` |
| `PlayerPosition` | ❌ | `C`, `F`, `G`, `C-F`, `F-C`, `F-G`, `G-F` | `` |
| `StarterBench` | ❌ | `Starters` or `Bench` | `` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |
| `LastNGames` | ❌ | Last N games | `0` |
| `Month` | ❌ | Month number | `0` |
| `OpponentTeamID` | ❌ | Opponent filter | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `Country` | ❌ | Country name | `` |
| `Conference` | ❌ | `East` or `West` | `` |
| `Division` | ❌ | Division name | `` |
| `DraftYear` | ❌ | Draft year | `` |
| `DraftPick` | ❌ | Pick range | `` |
| `College` | ❌ | College name | `` |
| `Height` | ❌ | Height range | `` |
| `Weight` | ❌ | Weight range | `` |
| `PlayerExperience` | ❌ | `Rookie`, `Sophomore`, `Veteran` | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |

```bash
# All players, base stats per game
curl "https://stats.nba.com/stats/leaguedashplayerstats?Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&TeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`LeagueDashPlayerStats` headers (Base measure):** `PLAYER_ID`, `PLAYER_NAME`, `NICKNAME`, `TEAM_ID`, `TEAM_ABBREVIATION`, `AGE`, `GP`, `W`, `L`, `W_PCT`, `MIN`, `FGM`, `FGA`, `FG_PCT`, `FG3M`, `FG3A`, `FG3_PCT`, `FTM`, `FTA`, `FT_PCT`, `OREB`, `DREB`, `REB`, `AST`, `TOV`, `STL`, `BLK`, `BLKA`, `PF`, `PFD`, `PTS`, `PLUS_MINUS`, `NBA_FANTASY_PTS`, `DD2`, `TD3`, `WNBA_FANTASY_PTS`

---

## League Dash Team Stats

**VERIFIED** — Aggregated stats for all teams.

**Endpoint:** `GET /leaguedashteamstats`

Same parameters as `leaguedashplayerstats`, minus player-specific filters (`PlayerPosition`, `StarterBench`, `DraftYear`, `College`, `Height`, `Weight`, `PlayerExperience`, `Country`).

```bash
# All teams, advanced stats
curl "https://stats.nba.com/stats/leaguedashteamstats?Season=2024-25&SeasonType=Regular+Season&MeasureType=Advanced&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&TeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`LeagueDashTeamStats` key headers (Advanced):** `TEAM_ID`, `TEAM_NAME`, `GP`, `W`, `L`, `W_PCT`, `MIN`, `E_OFF_RATING`, `OFF_RATING`, `E_DEF_RATING`, `DEF_RATING`, `E_NET_RATING`, `NET_RATING`, `AST_PCT`, `AST_TOV`, `AST_RATIO`, `OREB_PCT`, `DREB_PCT`, `REB_PCT`, `TM_TOV_PCT`, `EFG_PCT`, `TS_PCT`, `E_PACE`, `PACE`, `PACE_PER40`, `POSS`, `PIE`

---

## League Game Finder

**VERIFIED** — Search for games by date range, team, or player criteria. Useful for resolving GameIDs.

**Endpoint:** `GET /leaguegamefinder`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `PlayerOrTeam` | ✅ | `T` (team) or `P` (player) | `T` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `LeagueID` | ✅ | `00` | `00` |
| `TeamID` | ❌ | Filter to team | `` |
| `PlayerID` | ❌ | Filter to player | `` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `03/01/2025` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `03/25/2025` |
| `Vs_TeamID` | ❌ | Opponent team ID | `` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `PORound` | ❌ | Playoff round | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |

```bash
curl "https://stats.nba.com/stats/leaguegamefinder?PlayerOrTeam=T&Season=2024-25&SeasonType=Regular+Season&LeagueID=00&DateFrom=03/01/2025&DateTo=03/25/2025" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`LeagueGameFinderTeamResults` headers:** `SEASON_ID`, `TEAM_ID`, `TEAM_ABBREVIATION`, `TEAM_NAME`, `GAME_ID`, `GAME_DATE`, `MATCHUP`, `WL`, `MIN`, `PTS`, `FGM`, `FGA`, `FG_PCT`, `FG3M`, `FG3A`, `FG3_PCT`, `FTM`, `FTA`, `FT_PCT`, `OREB`, `DREB`, `REB`, `AST`, `STL`, `BLK`, `TOV`, `PF`, `PLUS_MINUS`, `VIDEO_AVAILABLE`

---

## Draft History

**VERIFIED** — Full list of draft picks for a given year or all years.

**Endpoint:** `GET /drafthistory`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `Season` | ❌ | Draft year (4-digit) | `2024` |
| `TeamID` | ❌ | Filter by team | `0` |
| `RoundNum` | ❌ | `1` or `2` | `` |
| `RoundPick` | ❌ | Pick number within round | `` |
| `OverallPick` | ❌ | Overall pick number | `` |
| `College` | ❌ | College name filter | `` |
| `Country` | ❌ | Country filter | `` |
| `TopX` | ❌ | Top N picks only | `` |

```bash
# 2024 NBA draft
curl "https://stats.nba.com/stats/drafthistory?LeagueID=00&Season=2024" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`DraftHistory` headers:** `PERSON_ID`, `PLAYER_NAME`, `SEASON`, `ROUND_NUMBER`, `ROUND_PICK`, `OVERALL_PICK`, `DRAFT_TYPE`, `TEAM_ID`, `TEAM_CITY`, `TEAM_NAME`, `TEAM_ABBREVIATION`, `ORGANIZATION`, `ORGANIZATION_TYPE`, `PLAYER_PROFILE_FLAG`

**Sample row:**
```json
[1642365, "Zaccharie Risacher", "2024", 1, 1, 1, "Draft", 1610612737, "Atlanta", "Hawks", "ATL", "JL Bourg (France)", "International", 1]
```

> **Notes:**
> - `Season` is the year the draft took place (not the following NBA season)
> - Omitting `Season` returns the full draft history since ~1947
> - Historical picks (pre-1989) may have incomplete player profile data

---

## Common All Players

**VERIFIED** — All registered NBA players (active and historical).

**Endpoint:** `GET /commonallplayers`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `Season` | ✅ | Season string | `2024-25` |
| `IsOnlyCurrentSeason` | ✅ | `1` (active only) or `0` (all-time) | `1` |

```bash
# All active NBA players this season
curl "https://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2024-25&IsOnlyCurrentSeason=1" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"

# All-time player list
curl "https://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2024-25&IsOnlyCurrentSeason=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`CommonAllPlayers` headers:** `PERSON_ID`, `DISPLAY_LAST_COMMA_FIRST`, `DISPLAY_FIRST_LAST`, `ROSTERSTATUS`, `FROM_YEAR`, `TO_YEAR`, `PLAYERCODE`, `PLAYER_SLUG`, `TEAM_ID`, `TEAM_CITY`, `TEAM_NAME`, `TEAM_ABBREVIATION`, `TEAM_CODE`, `TEAM_SLUG`, `GAMES_PLAYED_FLAG`
