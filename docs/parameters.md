# Parameters Reference

> Quick-reference for all query parameters used across the NBA Stats API (`https://stats.nba.com/stats/`).

---

## Universal Parameters

These parameters appear across almost all endpoints.

| Parameter | Description | Values |
|-----------|-------------|--------|
| `LeagueID` | League selector | `00` (NBA) · `10` (WNBA) · `20` (G League) |
| `Season` | Season in `YYYY-YY` format | `2024-25`, `2023-24`, … |
| `SeasonType` | Regular vs postseason | `Regular Season` · `Playoffs` · `Pre Season` · `All Star` |
| `PerMode` | Stat aggregation mode | `PerGame` · `Totals` · `Per100Possessions` · `Per36` · `Per48` · `Per40` · `MinutesPer` |

---

## MeasureType Values

Used in dashboard and league dash endpoints.

| Value | Description |
|-------|-------------|
| `Base` | Traditional stats (Pts, Reb, Ast, etc.) |
| `Advanced` | OffRtg, DefRtg, NetRtg, TS%, PACE, PIE |
| `Misc` | 2nd chance pts, pts off TO, fast break pts |
| `Four Factors` | eFG%, TOV%, OREB%, FT rate (Dean Oliver model) |
| `Scoring` | Shot distribution by location and type |
| `Usage` | USG%, usage-adjusted stats |
| `Defense` | Defensive metrics and opponent allowed stats |
| `Opponent` | Opponent perspective (OPP_FGM, OPP_PTS, etc.) |

---

## SeasonType Values

| Value | Description |
|-------|-------------|
| `Regular Season` | NBA regular season |
| `Playoffs` | NBA playoffs |
| `Pre Season` | Preseason / exhibition games |
| `All Star` | All-Star weekend |

---

## Filter Parameters

These are optional on most endpoints.

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `DateFrom` | Start date filter | `03/01/2025` (MM/DD/YYYY) |
| `DateTo` | End date filter | `03/31/2025` |
| `LastNGames` | Only last N games (`0` = all) | `5`, `10`, `0` |
| `Month` | Calendar month number (`0` = all) | `1` through `12` |
| `SeasonSegment` | Half-season filter | `Pre All-Star` · `Post All-Star` |
| `Location` | Home or away games | `Home` · `Road` |
| `Outcome` | Win or loss games | `W` · `L` |
| `OpponentTeamID` | Filter by opponent team ID | `1610612747` |
| `VsConference` | Opponent conference | `East` · `West` |
| `VsDivision` | Opponent division | `Atlantic` · `Central` · `Southeast` · `Northwest` · `Pacific` · `Southwest` |
| `Period` | Quarter filter (`0` = all) | `1` · `2` · `3` · `4` |
| `PlusMinus` | Include plus/minus column | `Y` · `N` |
| `PaceAdjust` | Pace-adjusted stats | `Y` · `N` |
| `Rank` | Include league rank column | `Y` · `N` |

---

## Player-Specific Filters

Only available on `leaguedashplayerstats`, `leaguehustlestatsplayer`, and similar endpoints.

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `TeamID` | Filter to one team (`0` = all) | `1610612747` |
| `PlayerPosition` | Position filter | `C` · `F` · `G` · `C-F` · `F-C` · `F-G` · `G-F` |
| `StarterBench` | Starter or bench role | `Starters` · `Bench` |
| `PlayerExperience` | Experience level | `Rookie` · `Sophomore` · `Veteran` |
| `Height` | Height range | `LT 6-0` · `GT 6-10` |
| `Weight` | Weight range | `LT 200` · `GT 250` |
| `Country` | Country of origin | `USA` · `France` · `Serbia` |
| `College` | College | `Duke` · `Kentucky` |
| `DraftYear` | Draft year (4-digit) | `2021` |
| `DraftPick` | Pick range | `1-10` |

---

## Scope Parameter (leagueleaders)

| Value | Description |
|-------|-------------|
| `S` | Standard (qualified players, min minutes threshold) |
| `RS` | Rookies only |
| `SP` | Rookies and sophomores |

---

## Playoff Round Filter (PORound)

Used on player/team dashboard and hustle endpoints during playoffs.

| Value | Round |
|-------|-------|
| `1` | First Round |
| `2` | Second Round (Conference Semifinals) |
| `3` | Conference Finals |
| `4` | NBA Finals |

---

## GameID Format

| Prefix | Season Type |
|--------|------------|
| `001` | Preseason |
| `002` | Regular Season |
| `004` | Playoffs |

Example: `0022401063`
- `002` = Regular Season
- `24` = 2024-25 season
- `01063` = game number

---

## Season ID Format

`SeasonID` in standings and some dashboards uses `2YYYY`:
- `22024` = 2024-25 season
- `22023` = 2023-24 season

---

## Common Stat Column Names

| Column | Description |
|--------|-------------|
| `GP` | Games played |
| `W` / `L` | Wins / Losses |
| `W_PCT` | Win percentage |
| `MIN` | Minutes (game) or total minutes (season) |
| `FGM` / `FGA` | Field goals made / attempted |
| `FG_PCT` | FG percentage |
| `FG3M` / `FG3A` | 3-pointers made / attempted |
| `FG3_PCT` | 3-point percentage |
| `FTM` / `FTA` | Free throws made / attempted |
| `FT_PCT` | Free throw percentage |
| `OREB` | Offensive rebounds |
| `DREB` | Defensive rebounds |
| `REB` | Total rebounds |
| `AST` | Assists |
| `TOV` | Turnovers |
| `STL` | Steals |
| `BLK` | Blocks |
| `BLKA` | Blocked attempts (shots blocked on player) |
| `PF` | Personal fouls |
| `PFD` | Personal fouls drawn |
| `PTS` | Points |
| `PLUS_MINUS` | Plus/minus |
| `OFF_RATING` | Offensive rating (pts per 100 possessions) |
| `DEF_RATING` | Defensive rating (pts allowed per 100 possessions) |
| `NET_RATING` | Net rating (`OFF_RATING` − `DEF_RATING`) |
| `AST_PCT` | Assist percentage |
| `AST_TOV` | Assist-to-turnover ratio |
| `EFG_PCT` | Effective FG percentage |
| `TS_PCT` | True shooting percentage |
| `USG_PCT` | Usage percentage |
| `PACE` | Possessions per 48 minutes |
| `PIE` | Player Impact Estimate |
