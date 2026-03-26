# NBA Stats Public API Documentation

> Unofficial documentation for the NBA Stats API (`stats.nba.com`) — endpoints, required headers, parameters, and real examples.

**Disclaimer:** This is documentation for an undocumented public API. Not affiliated with the NBA. Use responsibly.

---

## Table of Contents

- [Base URL](#base-url)
- [Required Headers](#required-headers)
- [Quick Start](#quick-start)
- [Response Format](#response-format)
- [ID Formats](#id-formats)
- [Season Format](#season-format)
- [Endpoint Index](#endpoint-index)
  - [Game Endpoints](docs/game_endpoints.md)
  - [Player Endpoints](docs/player_endpoints.md)
  - [Team Endpoints](docs/team_endpoints.md)
  - [League Endpoints](docs/league_endpoints.md)
  - [Advanced Analytics](docs/advanced_endpoints.md)
- [Parameters Reference](docs/parameters.md)

---

## Base URL

```
https://stats.nba.com/stats/
```

All endpoints are `GET` requests. No authentication required, but strict **header validation** is enforced (see below).

---

## Required Headers

The NBA Stats API uses a Web Application Firewall (WAF) that blocks requests without proper browser headers. **All requests require these headers** or you will receive a `403 Forbidden` or empty response.

| Header | Required Value |
|--------|---------------|
| `Accept` | `application/json, text/plain, */*` |
| `Accept-Language` | `en-US,en;q=0.9` |
| `Origin` | `https://www.nba.com` |
| `Referer` | `https://www.nba.com/` |
| `User-Agent` | Any modern browser string |
| `x-nba-stats-origin` | `stats` |
| `x-nba-stats-token` | `true` |

```python
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}
```

> ⚠️ The `x-nba-stats-origin` and `x-nba-stats-token` headers are non-standard NBA-specific headers. Without them, many endpoints return empty result sets or errors even when other headers are correct.

---

## Quick Start

```bash
# Today's scoreboard
curl "https://stats.nba.com/stats/scoreboardv2?GameDate=2025-03-26&LeagueID=00&DayOffset=0" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"

# LeBron James career stats
curl "https://stats.nba.com/stats/playercareerstats?PlayerID=2544&PerMode=PerGame&LeagueID=00" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"

# Current standings
curl "https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2024-25&SeasonType=Regular+Season" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"

# Scoring leaders
curl "https://stats.nba.com/stats/leagueleaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2024-25&SeasonType=Regular+Season&StatCategory=PTS" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Response Format

Most endpoints use the `resultSets` format:

```json
{
  "resource": "endpoint_name",
  "parameters": { ... },
  "resultSets": [
    {
      "name": "DataSetName",
      "headers": ["COL_A", "COL_B", "COL_C"],
      "rowSet": [
        ["value_a", "value_b", "value_c"]
      ]
    }
  ]
}
```

> **Note:** Rows are arrays, not objects. Match values to headers by index. For example, `row[headers.indexOf("PTS")]` to get points.

Newer `v3` endpoints (e.g., `scoreboardv3`, `boxscoretraditionalv3`, `playbyplayv3`) return named JSON objects instead:

```json
{
  "scoreboard": {
    "gameDate": "2025-03-26",
    "games": [ ... ]
  }
}
```

---

## ID Formats

| ID Type | Format | Example |
|---------|--------|---------|
| `GameID` | 10-digit string | `0022401045` |
| `TeamID` | 10-digit string starting with `161` | `1610612747` (Lakers) |
| `PlayerID` | Variable-length integer string | `2544` (LeBron James) |
| `LeagueID` | 2-digit string | `00` (NBA), `10` (WNBA), `20` (G League) |

### GameID Prefix Key

| Prefix | Meaning |
|--------|---------|
| `001` | Preseason |
| `002` | Regular Season |
| `004` | Playoffs |

> The digits after the prefix encode the season year. `002240XXXX` = 2024-25 Regular Season.

---

## Season Format

All season parameters use the `YYYY-YY` format:

| String | Season |
|--------|--------|
| `2024-25` | 2024-25 NBA season |
| `2023-24` | 2023-24 NBA season |

---

## Endpoint Index

| Category | File | Key Endpoints |
|----------|------|---------------|
| 🏀 Game | [game_endpoints.md](docs/game_endpoints.md) | Scoreboard, Boxscore, Play-by-Play, Win Probability |
| 👤 Player | [player_endpoints.md](docs/player_endpoints.md) | Game Log, Career Stats, Shot Chart, Player Info |
| 🏢 Team | [team_endpoints.md](docs/team_endpoints.md) | Team Stats, Roster, Lineups, Schedule |
| 🏆 League | [league_endpoints.md](docs/league_endpoints.md) | Standings, Leaders, Draft, Game Finder |
| 📊 Advanced | [advanced_endpoints.md](docs/advanced_endpoints.md) | Hustle, Tracking, Advanced Splits, Defense |

---

## Common Team IDs

| Team | ID |
|------|----|
| Atlanta Hawks | `1610612737` |
| Boston Celtics | `1610612738` |
| Brooklyn Nets | `1610612751` |
| Charlotte Hornets | `1610612766` |
| Chicago Bulls | `1610612741` |
| Cleveland Cavaliers | `1610612739` |
| Dallas Mavericks | `1610612742` |
| Denver Nuggets | `1610612743` |
| Detroit Pistons | `1610612765` |
| Golden State Warriors | `1610612744` |
| Houston Rockets | `1610612745` |
| Indiana Pacers | `1610612754` |
| LA Clippers | `1610612746` |
| Los Angeles Lakers | `1610612747` |
| Memphis Grizzlies | `1610612763` |
| Miami Heat | `1610612748` |
| Milwaukee Bucks | `1610612749` |
| Minnesota Timberwolves | `1610612750` |
| New Orleans Pelicans | `1610612740` |
| New York Knicks | `1610612752` |
| Oklahoma City Thunder | `1610612760` |
| Orlando Magic | `1610612753` |
| Philadelphia 76ers | `1610612755` |
| Phoenix Suns | `1610612756` |
| Portland Trail Blazers | `1610612757` |
| Sacramento Kings | `1610612758` |
| San Antonio Spurs | `1610612759` |
| Toronto Raptors | `1610612761` |
| Utah Jazz | `1610612762` |
| Washington Wizards | `1610612764` |

---

## Notable Player IDs

| Player | ID |
|--------|----|
| LeBron James | `2544` |
| Stephen Curry | `201939` |
| Kevin Durant | `201142` |
| Nikola Jokic | `203999` |
| Giannis Antetokounmpo | `203507` |
| Luka Doncic | `1629029` |
| Ja Morant | `1629630` |
| Jayson Tatum | `1628369` |
| Shai Gilgeous-Alexander | `1628983` |
| Victor Wembanyama | `1641705` |

---

## Rate Limiting

No official rate limits are published. In practice:
- ~30 requests/minute from a single IP without delays is generally safe
- Exceeding this may trigger a temporary `403` or `429` response
- Always include the required headers — missing `x-nba-stats-token` or `Referer` is the most common cause of empty responses
- Add `time.sleep(0.6)` between requests in scripts

---

*Last updated: March 2026 · Verified against 2024-25 season data*
