# Additional Domains / Related Endpoint Families

> All data below was discovered by reverse-engineering real browser requests and probing endpoints from `nba.com` on 2026-03-26. Accessibility statuses are observed, not guaranteed.

The NBA's data infrastructure spans several domains beyond the primary stats API. Each serves a distinct role — live data delivery, static assets, internal microservices, or partner-facing APIs.

---

## Domain Overview

| Domain | Accessibility | Purpose |
|--------|--------------|---------|
| `stats.nba.com/stats/` | ✅ Public (WAF-gated) | Primary historical + analytical stats API |
| `data.nba.com` | ✅ Public (no auth) | Live game data, mobile JSON feeds |
| `cdn.nba.com` | ✅ Public CDN | Player headshots, logos, video thumbnails |
| `nba.cloud` | 🔒 Internal only | Microservice backing v3 endpoints |
| `feeds.nba.com` | ❌ Shut down | Legacy XML/JSON feeds (ERR_CONNECTION_CLOSED) |
| `api.nba.com` | 🔒 Partner API (401) | Business data, partner integrations |
| `stats.nba.com/js/data/` | ⚠️ Deprecated | Pre-built JSON flat files (mostly 404) |
| `dleague.nba.com` | 🔒 Restricted | G League historical data |

---

## 1. `stats.nba.com/stats/` — Primary Stats API

**Accessibility:** Public (WAF-gated)

The main subject of this documentation. Serves all historical, analytical, and aggregated statistical data. Requires specific HTTP headers to bypass the WAF:

```
Referer: https://www.nba.com/
x-nba-stats-origin: stats
x-nba-stats-token: true
```

Endpoints follow two format generations:
- **v2 / unversioned** — `resultSets[i].headers` + `rowSet` 2D array
- **v3** — nested named JSON objects (camelCase keys)

See [versions.md](versions.md) for the full comparison.

---

## 2. `data.nba.com` — Live Game Data Feeds

**Accessibility:** ✅ Public — no WAF headers required

Delivers fast, cached JSON files used by the NBA mobile app and NBA.com homepage scoreboard. Data refreshes every 10–30 seconds during live games. This domain does **not** require the `x-nba-stats-origin` or `Referer` headers.

**Key endpoints:**

```bash
# Today's scores — all games, scores, status
GET https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{SEASON}/scores/00_todays_scores.json

# Single game live box score (v2015 format)
GET https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{SEASON}/scores/gamedetail/{GAME_ID}_gamedetail.json

# Team schedules
GET https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{SEASON}/teams/{TEAM_ID}_config.json

# League schedule (full season)
GET https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{SEASON}/league/{LEAGUE_ID}_full_schedule.json
```

Replace `{SEASON}` with e.g. `2024`, `{GAME_ID}` with a 10-digit game ID.

**Response format:** Proprietary flat JSON (not `resultSets`). Game objects use abbreviated keys (`vls`=visitor, `hls`=home, `s`=score, `q1`–`q4`=quarter scores).

**Sample response:**
```json
{
  "gs": {
    "gdte": "2025-03-26",
    "an": "Chase Center",
    "gid": "0022401063",
    "gcode": "20250326/CHAPAT",
    "stt": "Final",
    "vls": { "s": "107", "q1": "28", "q2": "25", "q3": "27", "q4": "27", "tc": "New York", "tn": "Knicks", "ta": "NYK" },
    "hls": { "s": "109", "q1": "31", "q2": "24", "q3": "28", "q4": "26", "tc": "Charlotte", "tn": "Hornets", "ta": "CHA" }
  }
}
```

**Relationship to main API:** Complements `scoreboardv2`/`scoreboardv3` for real-time use cases. Lower latency, no auth requirement, but far less detail (no player-level box score).

---

## 3. `cdn.nba.com` — Static Assets CDN

**Accessibility:** ✅ Public — no auth

The NBA's primary content delivery network for all static media. Used by every NBA-related product to serve visuals.

**Key URL patterns:**

```
# Player headshots (PLAYER_ID from any stats endpoint)
https://cdn.nba.com/headshots/nba/latest/1040x760/{PLAYER_ID}.png
https://cdn.nba.com/headshots/nba/latest/260x190/{PLAYER_ID}.png

# Team logos (SVG)
https://cdn.nba.com/logos/nba/{TEAM_ID}/global/L/logo.svg

# Team logos (PNG, multiple sizes)
https://cdn.nba.com/logos/nba/{TEAM_ID}/primary/L/logo.png

# G League player headshots
https://cdn.nba.com/headshots/gleague/latest/1040x760/{PLAYER_ID}.png
```

**Examples:**

| Asset | URL |
|-------|-----|
| LeBron James headshot | `https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png` |
| Lakers logo | `https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg` |
| Celtics primary logo | `https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.png` |

**Relationship to main API:** The stats API returns `PLAYER_ID` and `TEAM_ID` as integers — plug them directly into these URL templates to get images. No separate lookup needed.

---

## 4. `nba.cloud` — Internal Microservice (v3 Backend)

**Accessibility:** 🔒 Internal — not publicly routable

Discovered from the `meta.request` field embedded in every v3 endpoint response:

```json
{
  "meta": {
    "version": 1,
    "request": "http://nba.cloud/league/00/2025/03/25/scoreboard?Format=json",
    "time": "2025-07-03T07:11:03.113Z"
  }
}
```

This is the **internal microservice URL** that `stats.nba.com` calls on the backend when you request a v3 endpoint. The route structure reveals the v3 internal API schema:

| Discovered internal route | Used by `stats.nba.com` endpoint |
|---|---|
| `http://nba.cloud/league/00/{YYYY}/{MM}/{DD}/scoreboard` | `scoreboardv3` |
| `http://nba.cloud/games/{GAME_ID}/boxscoretraditional` | `boxscoretraditionalv3` |
| `http://nba.cloud/games/{GAME_ID}/playbyplay` | `playbyplayv3` |

Attempting to hit `nba.cloud` directly from the public internet returns no response — the domain is not publicly routable and is likely on a private VPC. `stats.nba.com` acts as the public-facing reverse proxy.

**Why this matters:** The internal URL pattern reveals that NBA's v3 data architecture uses a RESTful path structure (`/games/{id}/...`) rather than query-parameter-heavy URLs. This is a useful signal for predicting undocumented v3 endpoint paths.

---

## 5. `api.nba.com` — Partner API (Private)

**Accessibility:** 🔒 Private — `401 Unauthorized`

A modern REST API distinct from `stats.nba.com`. Likely serves official NBA app clients and verified business partners. Returns `401` with no API key; the auth mechanism is unknown (likely Bearer token or subscription-based API key).

**Known endpoints (from public references):**

```
GET https://api.nba.com/teams?league=standard&season=2024
GET https://api.nba.com/players?league=standard&season=2024
GET https://api.nba.com/standings?league=standard&season=2024
```

**Relationship to main API:** Appears to be a newer, more tightly controlled sibling of `stats.nba.com`. May share the same data warehouse but with restricted access.

---

## 6. `feeds.nba.com` — Shut Down / Legacy

**Accessibility:** ❌ `ERR_CONNECTION_CLOSED`

Previously hosted RSS-style JSON feeds for scores, news, and schedules used by the old NBA.com frontend. These endpoints are now completely inaccessible — the domain no longer responds to HTTP connections.

**Historical endpoints (no longer work):**

```
https://feeds.nba.com/nba/prod/v1/today.json
https://feeds.nba.com/nba/prod/v1/{YEAR}/{GAME_ID}/boxscore.json
https://feeds.nba.com/nba/prod/v2/{YEAR}/{DATE}/scoreboard.json
```

**Relationship to main API:** Superseded by `data.nba.com` for live feeds and `stats.nba.com` for historical data. Any documentation referencing `feeds.nba.com` is outdated.

---

## 7. `stats.nba.com/js/data/` — Deprecated Flat Files

**Accessibility:** ⚠️ Mostly 404 / returns `Content Unavailable`

A legacy path that served pre-computed JSON blobs used by specific JavaScript chart widgets on the stats.nba.com website. No longer actively maintained.

**Historical paths (mostly dead):**

```
https://stats.nba.com/js/data/ptsdxg/team_all_2024_2025_regular.json
https://stats.nba.com/js/data/sportvu/{season}/...
```

---

## Summary

For practical use, only three domains are relevant:

| Domain | Use case |
|--------|----------|
| `stats.nba.com/stats/` | All historical stats, player/team/game data |
| `data.nba.com` | Real-time live scores, no auth needed |
| `cdn.nba.com` | Player headshots and team logos via ID |
