# Clutch & Situational Stats Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## League Dash Player Clutch

**VERIFIED** — Player stats filtered to clutch situations (last N minutes, within N points).

**Endpoint:** `GET /leaguedashplayerclutch`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `MeasureType` | ✅ | `Base`, `Advanced`, `Misc`, `Four Factors`, `Scoring`, `Opponent`, `Usage`, `Defense` | `Base` |
| `PerMode` | ✅ | `PerGame`, `Totals`, `Per100Possessions`, etc. | `PerGame` |
| `ClutchTime` | ✅ | Time window for clutch situations | `Last 5 Minutes` |
| `AheadBehind` | ✅ | Score differential filter | `Ahead or Behind` |
| `PointDiff` | ✅ | Max point diff for clutch bucket | `5` |
| `PlusMinus` | ✅ | `Y` / `N` | `N` |
| `PaceAdjust` | ✅ | `Y` / `N` | `N` |
| `Rank` | ✅ | `Y` / `N` | `N` |
| `LeagueID` | ✅ | `00` | `00` |
| `Period` | ❌ | Quarter (`0` = all) | `0` |
| `Month` | ❌ | Month number | `0` |
| `LastNGames` | ❌ | Last N games | `0` |
| `OpponentTeamID` | ❌ | Opponent filter | `0` |
| `TeamID` | ❌ | Filter to team | `0` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `Conference` | ❌ | `East` or `West` | `` |
| `Division` | ❌ | Division name | `` |
| `StarterBench` | ❌ | `Starters` or `Bench` | `` |
| `PlayerPosition` | ❌ | `C`, `F`, `G` | `` |
| `VsConference` | ❌ | `East` or `West` | `` |
| `VsDivision` | ❌ | Division name | `` |
| `College` | ❌ | College name | `` |
| `Country` | ❌ | Country | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |
| `PORound` | ❌ | Playoff round | `` |

**`ClutchTime` values:**
`Last 5 Minutes` · `Last 4 Minutes` · `Last 3 Minutes` · `Last 2 Minutes` · `Last 1 Minute` · `Last 30 Seconds` · `Last 10 Seconds`

**`AheadBehind` values:**
`Ahead or Behind` · `Behind or Tied` · `Ahead or Tied`

```bash
# Players in last 5 minutes, within 5 points
curl "https://stats.nba.com/stats/leaguedashplayerclutch?Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&ClutchTime=Last+5+Minutes&AheadBehind=Ahead+or+Behind&PointDiff=5&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&TeamID=0&Period=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`LeagueDashPlayerClutch` headers (Base):** Same columns as `leaguedashplayerstats` — `GROUP_SET`, `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `TEAM_ABBREVIATION`, `AGE`, `GP`, `W`, `L`, `W_PCT`, `MIN`, `FGM`, `FGA`, `FG_PCT`, `FG3M`, `FG3A`, `FG3_PCT`, `FTM`, `FTA`, `FT_PCT`, `OREB`, `DREB`, `REB`, `AST`, `TOV`, `STL`, `BLK`, `BLKA`, `PF`, `PFD`, `PTS`, `PLUS_MINUS`

---

## League Dash Team Clutch

**VERIFIED** — Same as player clutch but team-level aggregates.

**Endpoint:** `GET /leaguedashteamclutch`

Same parameters as `leaguedashplayerclutch`, minus player-specific filters.

```bash
curl "https://stats.nba.com/stats/leaguedashteamclutch?Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&ClutchTime=Last+5+Minutes&AheadBehind=Ahead+or+Behind&PointDiff=5&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&TeamID=0&Period=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Player Dashboard by Clutch

**VERIFIED** — Clutch splits for a single player.

**Endpoint:** `GET /playerdashboardbyclutch`

Same parameters as `playerdashboardbygeneralsplits`, with added:

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `ClutchTime` | ✅ | Clutch window | `Last 5 Minutes` |
| `AheadBehind` | ✅ | Score situation | `Ahead or Behind` |
| `PointDiff` | ✅ | Max point diff | `5` |

```bash
curl "https://stats.nba.com/stats/playerdashboardbyclutch?PlayerID=2544&Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&ClutchTime=Last+5+Minutes&AheadBehind=Ahead+or+Behind&PointDiff=5&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## IST Standings

**VERIFIED** — In-Season Tournament (NBA Cup) group stage standings.

**Endpoint:** `GET /iststandings`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season` | `Regular Season` |

```bash
curl "https://stats.nba.com/stats/iststandings?LeagueID=00&Season=2024-25&SeasonType=Regular+Season" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

> **Notes:** Only relevant during the NBA Cup portion of the regular season (November–December). Returns `EastGroup` and `WestGroup` result sets with group standings.
