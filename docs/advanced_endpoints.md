# Advanced Analytics Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.

---

## Hustle Stats — Players

**VERIFIED** — Tracking-based hustle metrics: deflections, contested shots, charges drawn, screen assists, box-outs.

**Endpoint:** `GET /leaguehustlestatsplayer`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | `Regular Season` or `Playoffs` | `Regular Season` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `PerGame` |
| `LeagueID` | ✅ | `00` | `00` |
| `TeamID` | ❌ | Filter to one team | `0` |
| `OpponentTeamID` | ❌ | Filter by opponent | `0` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |
| `LastNGames` | ❌ | Last N games | `0` |
| `Month` | ❌ | Month number | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |
| `PlayerPosition` | ❌ | `C`, `F`, `G` | `` |
| `College` | ❌ | College name | `` |
| `Country` | ❌ | Country | `` |
| `Height` | ❌ | Height filter | `` |
| `Weight` | ❌ | Weight filter | `` |
| `PlayerExperience` | ❌ | `Rookie`, `Sophomore`, `Veteran` | `` |
| `StarterBench` | ❌ | `Starters` or `Bench` | `` |
| `PORound` | ❌ | Playoff round | `` |
| `Period` | ❌ | Quarter (`0`= all) | `0` |

```bash
curl "https://stats.nba.com/stats/leaguehustlestatsplayer?Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&LeagueID=00&TeamID=0&OpponentTeamID=0&LastNGames=0&Month=0&Period=0&DateFrom=&DateTo=&Location=&Outcome=&SeasonSegment=&DraftPick=&DraftYear=&GameScope=&GameSegment=&PlayerExperience=&PlayerPosition=&StarterBench=&VsConference=&VsDivision=&PORound=&College=&Country=&Height=&Weight=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`HustleStatsPlayer` headers:** `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `TEAM_ABBREVIATION`, `AGE`, `G`, `MIN`, `CONTESTED_SHOTS`, `CONTESTED_SHOTS_2PT`, `CONTESTED_SHOTS_3PT`, `DEFLECTIONS`, `CHARGES_DRAWN`, `SCREEN_ASSISTS`, `SCREEN_AST_PTS`, `OFF_LOOSE_BALLS_RECOVERED`, `DEF_LOOSE_BALLS_RECOVERED`, `LOOSE_BALLS_RECOVERED`, `OFF_BOXOUTS`, `DEF_BOXOUTS`, `BOX_OUT_PLAYER_REBS`, `BOX_OUT_TEAM_REBS`, `BOX_OUTS`

---

## Hustle Stats — Teams

**VERIFIED** — Team-level hustle metrics.

**Endpoint:** `GET /leaguehustlestatsteam`

Same parameters as `leaguehustlestatsplayer`.

```bash
curl "https://stats.nba.com/stats/leaguehustlestatsteam?Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&LeagueID=00&TeamID=0&OpponentTeamID=0&LastNGames=0&Month=0&Period=0&DateFrom=&DateTo=&Location=&Outcome=&SeasonSegment=&DraftPick=&DraftYear=&GameScope=&GameSegment=&PORound=&College=&Country=&Height=&Weight=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Player Tracking Stats (leaguedashptstats)

**VERIFIED** — Optical tracking data: speed/distance, touches, passes, pull-up shooting, drives, defense at the rim.

**Endpoint:** `GET /leaguedashptstats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `PerGame` |
| `PlayerOrTeam` | ✅ | `Player` or `Team` | `Player` |
| `PtMeasureType` | ✅ | Tracking category (see below) | `SpeedDistance` |
| `LeagueID` | ✅ | `00` | `00` |
| `TeamID` | ❌ | Filter to team | `0` |
| `DateFrom` | ❌ | `MM/DD/YYYY` | `` |
| `DateTo` | ❌ | `MM/DD/YYYY` | `` |
| `LastNGames` | ❌ | Last N games | `0` |
| `Month` | ❌ | Month number | `0` |
| `Location` | ❌ | `Home` or `Road` | `` |
| `Outcome` | ❌ | `W` or `L` | `` |
| `SeasonSegment` | ❌ | `Pre All-Star` or `Post All-Star` | `` |
| `PlayerPosition` | ❌ | `C`, `F`, `G` | `` |
| `StarterBench` | ❌ | `Starters` or `Bench` | `` |
| `OpponentTeamID` | ❌ | Opponent filter | `0` |
| `Period` | ❌ | Quarter (`0` = all) | `0` |

**`PtMeasureType` values:**

| Value | Data Returned |
|-------|--------------|
| `SpeedDistance` | Miles traveled, avg speed (off + def), distance |
| `Possessions` | Touches, front court touches, time of possession, elbow/paint touches |
| `CatchShoot` | Catch-and-shoot FGM/FGA/FG%, points |
| `PullUpShot` | Pull-up (off-dribble) FGM/FGA/FG%, points |
| `Defense` | Defensive at-rim contests, opponents FG% at rim |
| `Drives` | Drives, drive pts, drive FGM, drive assists, drive turnovers |
| `Passing` | Passes made, passes received, assists, secondary assists, bad passes |
| `ElbowTouch` | Elbow touches, elbow passes, scoring from elbow |
| `PostTouch` | Post touches, post-up points/FGs, passing from the post |
| `PaintTouch` | Paint touches, points/FGs from paint touches |
| `Efficiency` | True Shooting %, Effective FG%, passes per touch, points per touch |

```bash
# Player speed and distance
curl "https://stats.nba.com/stats/leaguedashptstats?Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&PlayerOrTeam=Player&PtMeasureType=SpeedDistance&LeagueID=00&TeamID=0&DateFrom=&DateTo=&LastNGames=0&Month=0&Location=&Outcome=&SeasonSegment=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&Weight=&PlayerExperience=&PlayerPosition=&StarterBench=&College=&Country=&OpponentTeamID=0&Period=0&PORound=&VsConference=&VsDivision=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"

# Player passing stats
curl "https://stats.nba.com/stats/leaguedashptstats?Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&PlayerOrTeam=Player&PtMeasureType=Passing&LeagueID=00&TeamID=0&DateFrom=&DateTo=&LastNGames=0&Month=0&Location=&Outcome=&SeasonSegment=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&Weight=&PlayerExperience=&PlayerPosition=&StarterBench=&College=&Country=&OpponentTeamID=0&Period=0&PORound=&VsConference=&VsDivision=" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`SpeedDistance` headers:** `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `TEAM_ABBREVIATION`, `AGE`, `GP`, `W`, `L`, `W_PCT`, `MIN`, `DIST_MILES`, `DIST_MILES_OFF`, `DIST_MILES_DEF`, `AVG_SPEED`, `AVG_SPEED_OFF`, `AVG_SPEED_DEF`

**`Passing` headers (key):** `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ABBREVIATION`, `GP`, `MIN`, `PASSES_MADE`, `PASSES_RECEIVED`, `AST`, `SECONDARY_AST`, `POTENTIAL_AST`, `AST_PCT`, `AST_ADJ`, `AST_TO_PASS_PCT`, `AST_TO_PASS_PCT_ADJ`, `BAD_PASS_TURNOVER`, `BAD_PASS_TO_TURNOVER_RATIO`

---

## Player Estimated Metrics (Advanced)

**VERIFIED** — Estimated versions of OffRtg, DefRtg, NetRtg with expanded accuracy using tracking + stats models.

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

**Key headers:** `PLAYER_ID`, `PLAYER_NAME`, `GP`, `W`, `L`, `MIN`, `E_OFF_RATING`, `E_DEF_RATING`, `E_NET_RATING`, `E_AST_RATIO`, `E_OREB_PCT`, `E_DREB_PCT`, `E_REB_PCT`, `E_TOV_PCT`, `E_USG_PCT`, `E_PACE`, `E_FG_PCT`, `GP_RANK`, `W_RANK`, `MIN_RANK`, `E_OFF_RATING_RANK`, `E_DEF_RATING_RANK`, `E_NET_RATING_RANK`

---

## League Dash Player Shot Locations

**VERIFIED** — Shot frequency and efficiency by zone (restricted area, mid-range, 3PT, etc.).

**Endpoint:** `GET /leaguedashplayerptshot`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `Season` | ✅ | Season string | `2024-25` |
| `SeasonType` | ✅ | Season type | `Regular Season` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `Totals` |
| `LeagueID` | ✅ | `00` | `00` |
| `GeneralRange` | ❌ | `Overall`, `CatchShoot`, `Pullup` | `Overall` |
| `TeamID` | ❌ | Filter to team | `0` |

```bash
curl "https://stats.nba.com/stats/leaguedashplayerptshot?Season=2024-25&SeasonType=Regular+Season&PerMode=Totals&LeagueID=00&GeneralRange=Overall&TeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Key headers:** `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `GP`, `G`, `FGA_FREQUENCY`, `FGM`, `FGA`, `FG_PCT`, `EFG_PCT`, `FG2A_FREQUENCY`, `FG2M`, `FG2A`, `FG2_PCT`, `FG3A_FREQUENCY`, `FG3M`, `FG3A`, `FG3_PCT`

---

## Synergy Play Types

**PARTIALLY VERIFIED** — Possessions categorized by play type (transition, isolation, post-up, P&R ball-handler, etc.).

**Endpoint:** `GET /synergyplaytypes`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `SeasonYear` | ✅ | 4-digit year | `2024` |
| `SeasonType` | ✅ | `Regular Season` or `Playoffs` | `Regular Season` |
| `PerMode` | ✅ | `PerGame` or `Totals` | `PerGame` |
| `PlayerOrTeam` | ✅ | `P` (player) or `T` (team) | `P` |
| `TypeGrouping` | ✅ | `offensive` or `defensive` | `offensive` |
| `PlayType` | ✅ | Play type category (see below) | `Transition` |

**`PlayType` values:**

| Value | Description |
|-------|-------------|
| `Transition` | Fast break possessions |
| `Isolation` | 1-on-1 isolations |
| `PRBallHandler` | Pick & Roll — ball handler |
| `PRRollman` | Pick & Roll — roll man |
| `Postup` | Post-up possessions |
| `Spotup` | Spot-up (catch and shoot) |
| `Handoff` | Off-ball handoff |
| `Cut` | Backdoor and basket cuts |
| `OffScreen` | Off-screen actions |
| `OffRebound` | Putback / tip opportunities |
| `Misc` | Other possessions |

```bash
curl "https://stats.nba.com/stats/synergyplaytypes?LeagueID=00&SeasonYear=2024&SeasonType=Regular+Season&PerMode=PerGame&PlayerOrTeam=P&TypeGrouping=offensive&PlayType=Transition" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`SynergyPlayType` headers:** `SEASON_ID`, `PLAYER_ID`, `PLAYER_NAME`, `TEAM_ID`, `TEAM_ABBREVIATION`, `PLAY_TYPE`, `TYPE_GROUPING`, `PERCENTILE`, `GP`, `POSS_PCT`, `PPP`, `FG_PCT`, `FT_POSS_PCT`, `TOV_POSS_PCT`, `SF_POSS_PCT`, `PLUSONE_POSS_PCT`, `SCORE_POSS_PCT`, `EFG_PCT`, `POSS`, `PTS`, `FGM`, `FGA`, `FGMX`

> **Note:** `SeasonYear` uses 4-digit year (e.g., `2024`) not the `YYYY-YY` format used by most other endpoints.

---

## Boxscore Player Tracking (In-Game)

**VERIFIED** — Player tracking stats for an individual game (speed, distance, touches, passes).

**Endpoint:** `GET /boxscoreplayertrackv2`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `GameID` | ✅ | 10-digit game ID | `0022401063` |

```bash
curl "https://stats.nba.com/stats/boxscoreplayertrackv2?GameID=0022401063" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`PlayerTrack` headers:** `GAME_ID`, `TEAM_ID`, `TEAM_ABBREVIATION`, `TEAM_CITY`, `PLAYER_ID`, `PLAYER_NAME`, `START_POSITION`, `COMMENT`, `MIN`, `SPD`, `DIST`, `ORBC`, `DRBC`, `RBC`, `TCHS`, `SAST`, `FTAST`, `PASS`, `AST`, `CFGM`, `CFGA`, `CFG_PCT`, `UFGM`, `UFGA`, `UFG_PCT`, `FG_PCT`, `DFGM`, `DFGA`, `DFG_PCT`

---

## League Dash Opponent Stats

**VERIFIED** — How each team performs defensively against opponents.

**Endpoint:** `GET /leaguedashteamstats`

Set `MeasureType=Opponent` to get opponent-perspective stats (points allowed, opponent FG%, etc.).

```bash
curl "https://stats.nba.com/stats/leaguedashteamstats?Season=2024-25&SeasonType=Regular+Season&MeasureType=Opponent&PerMode=PerGame&PlusMinus=N&PaceAdjust=N&Rank=N&LeagueID=00&LastNGames=0&Month=0&OpponentTeamID=0&TeamID=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`LeagueDashTeamStats` (Opponent) headers include:** `OPP_FGM`, `OPP_FGA`, `OPP_FG_PCT`, `OPP_FG3M`, `OPP_FG3A`, `OPP_FG3_PCT`, `OPP_FTM`, `OPP_FTA`, `OPP_FT_PCT`, `OPP_OREB`, `OPP_DREB`, `OPP_REB`, `OPP_AST`, `OPP_TOV`, `OPP_STL`, `OPP_BLK`, `OPP_BLKA`, `OPP_PF`, `OPP_PFD`, `OPP_PTS`
