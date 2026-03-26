# NBA Stats API Documentation

> Comprehensive reference for the unofficial NBA Stats API — endpoints, parameters, required headers, and real examples.

---

## 📁 File Index

### Root

| File | Description |
|------|-------------|
| [README.md](../README.md) | Full overview — base URL, required headers, quick start, ID formats, team/player ID tables |

### Endpoint Reference (`docs/`)

| File | Coverage |
|------|----------|
| [game_endpoints.md](game_endpoints.md) | Scoreboard v2/v3, Boxscore (Traditional, Advanced, variants), Play-By-Play v2/v3, Win Probability, Game Summary |
| [player_endpoints.md](player_endpoints.md) | Player Info, Career Stats, Game Log, Dashboard, Player vs. Player, Shot Chart, Estimated Metrics |
| [team_endpoints.md](team_endpoints.md) | Roster, Game Log, Dashboard Splits, Year-Over-Year, Team Lineups, League Lineups, Team List |
| [league_endpoints.md](league_endpoints.md) | Standings, Leaders, League Dash Player/Team Stats, Game Finder, Draft History, All Players |
| [advanced_endpoints.md](advanced_endpoints.md) | Hustle Stats, Player Tracking (all `PtMeasureType`s), Synergy Play Types, In-Game Tracking, Opponent Stats |
| [clutch_situational_endpoints.md](clutch_situational_endpoints.md) | Player & Team Clutch Stats, Player Clutch Dashboard, IST (NBA Cup) Standings |
| [franchise_historical_endpoints.md](franchise_historical_endpoints.md) | Franchise History, Franchise Leaders/Players, Team Details, All-Time Leaders, Game Rotation, Player Awards, Player Compare |
| [draft_combine_endpoints.md](draft_combine_endpoints.md) | Draft Combine Stats, Anthro, Drills, Spot Shooting, Non-Stationary Shooting, Draft Board |
| [parameters.md](parameters.md) | Full parameter reference — MeasureType, SeasonType, PerMode, all filters, column definitions |

---

## 🚀 Quick Links

| Data | Endpoint |
|------|----------|
| Today's scores | `https://stats.nba.com/stats/scoreboardv2?GameDate={YYYY-MM-DD}&LeagueID=00&DayOffset=0` |
| Scoreboard (v3 format) | `https://stats.nba.com/stats/scoreboardv3?GameDate={YYYY-MM-DD}&LeagueID=00` |
| Boxscore | `https://stats.nba.com/stats/boxscoretraditionalv2?GameID={GAME_ID}&StartPeriod=0&EndPeriod=14&StartRange=0&EndRange=28800&RangeType=0` |
| Play-by-play | `https://stats.nba.com/stats/playbyplayv2?GameID={GAME_ID}&StartPeriod=1&EndPeriod=4` |
| Win probability | `https://stats.nba.com/stats/winprobabilitypbp?GameID={GAME_ID}&RunType=each+second` |
| Player career stats | `https://stats.nba.com/stats/playercareerstats?PlayerID={ID}&PerMode=PerGame&LeagueID=00` |
| Player game log | `https://stats.nba.com/stats/playergamelog?PlayerID={ID}&Season=2024-25&SeasonType=Regular+Season&LeagueID=00` |
| Shot chart | `https://stats.nba.com/stats/shotchartdetail?PlayerID={ID}&Season=2024-25&SeasonType=Regular+Season&TeamID=0&LeagueID=00&ContextMeasure=FGA` |
| Team roster | `https://stats.nba.com/stats/commonteamroster?TeamID={ID}&Season=2024-25&LeagueID=00` |
| Standings | `https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2024-25&SeasonType=Regular+Season` |
| Scoring leaders | `https://stats.nba.com/stats/leagueleaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2024-25&SeasonType=Regular+Season&StatCategory=PTS` |
| League player stats | `https://stats.nba.com/stats/leaguedashplayerstats?Season=2024-25&SeasonType=Regular+Season&MeasureType=Base&PerMode=PerGame&LeagueID=00` |
| League team stats | `https://stats.nba.com/stats/leaguedashteamstats?Season=2024-25&SeasonType=Regular+Season&MeasureType=Advanced&PerMode=PerGame&LeagueID=00` |
| Lineups | `https://stats.nba.com/stats/leaguedashlineups?Season=2024-25&SeasonType=Regular+Season&MeasureType=Advanced&PerMode=Per100Possessions&GroupQuantity=5&LeagueID=00` |
| Hustle stats | `https://stats.nba.com/stats/leaguehustlestatsplayer?Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&LeagueID=00` |
| Tracking (speed) | `https://stats.nba.com/stats/leaguedashptstats?Season=2024-25&SeasonType=Regular+Season&PerMode=PerGame&PlayerOrTeam=Player&PtMeasureType=SpeedDistance&LeagueID=00` |
| Draft history | `https://stats.nba.com/stats/drafthistory?LeagueID=00&Season=2024` |
| All players | `https://stats.nba.com/stats/commonallplayers?LeagueID=00&Season=2024-25&IsOnlyCurrentSeason=1` |
