# CHANGELOG

All documented endpoints and additions to the NBA Stats API reference.

---

## [1.1.0] — March 2026

### Added (Research Expansion)

**Clutch & Situational Endpoints**
- `leaguedashplayerclutch` — Player stats in clutch situations (fully parameterized: ClutchTime, AheadBehind, PointDiff)
- `leaguedashteamclutch` — Team-level clutch stats
- `playerdashboardbyclutch` — Individual player clutch splits
- `iststandings` — NBA Cup (In-Season Tournament) group stage standings

**Franchise & Historical Endpoints**
- `franchisehistory` — Win/loss, playoff appearances, and titles for all active and defunct franchises
- `franchiseleaders` — Career all-time leaders for a franchise
- `franchiseplayers` — All players who have appeared for a franchise
- `teamdetails` — Arena, ownership, championships, retired jerseys, Hall of Famers, social links
- `alltimeleadersgrids` — All-time career leaders across 15+ stat categories
- `gamerotation` — Full substitution timeline (who was on court, when, points scored per stint)
- `playerawards` — All NBA awards won by a player
- `playercompare` — Side-by-side stat comparison between player groups
- `commonplayoffseries` — All playoff series matchups for a season

**Draft Combine Endpoints**
- `draftcombinestats` — Combined anthropometric measurements + all drill results
- `draftcombineplayeranthro` — Anthropometrics only (height, wingspan, reach, weight, body fat)
- `draftcombinedrillresults` — Athleticism drills (sprint, agility, vertical, bench press)
- `draftcombinespotshooting` — Stationary spot shooting % from 3 distances
- `draftcombinenonstationaryshooting` — Off-dribble and on-the-move shooting
- `draftboard` — Live draft board with player rankings

---

## [1.0.0] — March 2026

### Initial Release

**Game Endpoints**
- `scoreboardv2` — Daily scoreboard with game headers, linescores, team leaders
- `scoreboardv3` — v3 format scoreboard with clean JSON object
- `boxscoretraditionalv2` — Traditional player/team box score
- `boxscoreadvancedv2` — Advanced in-game metrics (OffRtg, DefRtg, TS%, PACE)
- `boxscorescoringv2` — Scoring breakdown by shot type
- `boxscoremisc v2` — Miscellaneous game stats (PTS off TO, 2nd chance PTS)
- `boxscorefourfactorsv2` — Four factors per game
- `boxscoreusagev2` — Usage rate in game context
- `boxscoretraditionalv3` — Traditional boxscore in v3 format
- `boxscoreadvancedv3` — Advanced boxscore in v3 format
- `boxscorematchupsv3` — Matchup-level player tracking in v3 format
- `playbyplayv2` — Full play-by-play event log
- `playbyplayv3` — v3 format play-by-play with action types and qualifiers
- `winprobabilitypbp` — Second-by-second win probability
- `boxscoresummaryv2` — Game summary, officials, inactive players

**Player Endpoints**
- `commonplayerinfo` — Player biography and headline stats
- `playercareerstats` — Season-by-season and career totals
- `playergamelog` — Game-by-game stats for a player
- `playerdashboardbyyearoveryear` — Annual performance splits
- `playerdashboardbygeneralsplits` — Home/away, W/L, and other splits
- `playervsplayer` — Head-to-head stats between two players
- `shotchartdetail` — Shot coordinates, zone, type, and result
- `playerestimatedmetrics` — Estimated OffRtg, DefRtg, NetRtg

**Team Endpoints**
- `commonteamroster` — Current roster and coaching staff
- `teamgamelog` — Game-by-game results for a team
- `teamdashboardbygeneralsplits` — Team splits (home/away, W/L, month, etc.)
- `teamdashboardbyyearoveryear` — Year-over-year team performance trends
- `teamvsplayer` — Team stats when facing a specific player
- `teamdashlineups` — 2–5 man lineup stats for a team
- `leaguedashlineups` — League-wide lineup stats
- `commonteamyears` — All team IDs and active year ranges

**League Endpoints**
- `leaguestandingsv3` — Full conference and division standings
- `leagueleaders` — Stat category leaders (note: `resultSet` not `resultSets`)
- `leaguedashplayerstats` — All-player aggregated stats with full filter set
- `leaguedashteamstats` — All-team aggregated stats with full filter set
- `leaguegamefinder` — Game search by date, team, player criteria
- `drafthistory` — Full draft pick history since 1947
- `commonallplayers` — All registered NBA players (current or historical)

**Advanced Analytics Endpoints**
- `leaguehustlestatsplayer` — Player hustle metrics (deflections, contested shots, charges, screen assists, box-outs)
- `leaguehustlestatsteam` — Team-level hustle metrics
- `leaguedashptstats` — Optical tracking stats (11 `PtMeasureType` values)
- `leaguedashplayerptshot` — Shot frequency and efficiency by zone
- `synergyplaytypes` — Synergy play-type breakdown (isolation, P&R, post-up, etc.)
- `boxscoreplayertrackv2` — In-game player tracking (speed, distance, touches, passes)
- `leaguedashteamstats` (Opponent) — Opponent-allowed stats per team
