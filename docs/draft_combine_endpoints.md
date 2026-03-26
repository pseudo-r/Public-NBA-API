# Draft Combine Endpoints

> All endpoints use base URL `https://stats.nba.com/stats/`. See [README](../README.md) for required headers.
> Note: `SeasonYear` in this family uses `YYYY-YY` format (e.g., `2024-25`), not the 4-digit draft year.

---

## Draft Combine Stats (Combined)

**VERIFIED** — All anthropometric measurements and drill results for draft combine participants in a single endpoint.

**Endpoint:** `GET /draftcombinestats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `SeasonYear` | ✅ | Season in `YYYY-YY` format | `2024-25` |

```bash
curl "https://stats.nba.com/stats/draftcombinestats?LeagueID=00&SeasonYear=2024-25" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**`DraftCombineStats` headers:** `SEASON`, `PLAYER_ID`, `FIRST_NAME`, `LAST_NAME`, `PLAYER_NAME`, `POSITION`, `HEIGHT_WO_SHOES`, `HEIGHT_WO_SHOES_FT_IN`, `HEIGHT_W_SHOES`, `HEIGHT_W_SHOES_FT_IN`, `WEIGHT`, `WINGSPAN`, `WINGSPAN_FT_IN`, `STANDING_REACH`, `STANDING_REACH_FT_IN`, `BODY_FAT_PCT`, `HAND_LENGTH`, `HAND_WIDTH`, `STANDING_VERTICAL_LEAP`, `MAX_VERTICAL_LEAP`, `LANE_AGILITY_TIME`, `MODIFIED_LANE_AGILITY_TIME`, `THREE_QUARTER_SPRINT`, `BENCH_PRESS`, `SPOT_FIFTEEN_CORNER_LEFT`, `SPOT_FIFTEEN_BREAK_LEFT`, `SPOT_FIFTEEN_TOP_KEY`, `SPOT_FIFTEEN_BREAK_RIGHT`, `SPOT_FIFTEEN_CORNER_RIGHT`, `SPOT_COLLEGE_CORNER_LEFT`, `SPOT_COLLEGE_BREAK_LEFT`, `SPOT_COLLEGE_TOP_KEY`, `SPOT_COLLEGE_BREAK_RIGHT`, `SPOT_COLLEGE_CORNER_RIGHT`, `SPOT_NBA_CORNER_LEFT`, `SPOT_NBA_BREAK_LEFT`, `SPOT_NBA_TOP_KEY`, `SPOT_NBA_BREAK_RIGHT`, `SPOT_NBA_CORNER_RIGHT`, `OFF_DRIB_FIFTEEN_BREAK_LEFT`, `OFF_DRIB_FIFTEEN_TOP_KEY`, `OFF_DRIB_FIFTEEN_BREAK_RIGHT`, `OFF_DRIB_COLLEGE_BREAK_LEFT`, `OFF_DRIB_COLLEGE_TOP_KEY`, `OFF_DRIB_COLLEGE_BREAK_RIGHT`, `ON_MOVE_FIFTEEN`, `ON_MOVE_COLLEGE`

---

## Draft Combine Player Anthro

**VERIFIED** — Anthropometric measurements only (heights, wingspan, weight, etc.) without shooting drill results.

**Endpoint:** `GET /draftcombineplayeranthro`

Same parameters as `draftcombinestats`.

```bash
curl "https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&SeasonYear=2024-25" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Draft Combine Drill Results

**VERIFIED** — Athleticism drill results only (sprint, agility, vertical leap, bench press).

**Endpoint:** `GET /draftcombinedrillresults`

Same parameters as `draftcombinestats`.

```bash
curl "https://stats.nba.com/stats/draftcombinedrillresults?LeagueID=00&SeasonYear=2024-25" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Key headers:** `PLAYER_ID`, `PLAYER_NAME`, `POSITION`, `STANDING_VERTICAL_LEAP`, `MAX_VERTICAL_LEAP`, `LANE_AGILITY_TIME`, `MODIFIED_LANE_AGILITY_TIME`, `THREE_QUARTER_SPRINT`, `BENCH_PRESS`

---

## Draft Combine Spot Shooting

**VERIFIED** — Stationary spot-up shooting percentages from 15-foot, college 3-point, and NBA 3-point distances.

**Endpoint:** `GET /draftcombinespotshooting`

Same parameters as `draftcombinestats`.

```bash
curl "https://stats.nba.com/stats/draftcombinespotshooting?LeagueID=00&SeasonYear=2024-25" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Draft Combine Non-Stationary Shooting

**VERIFIED** — Off-dribble and on-the-move shooting results from the combine.

**Endpoint:** `GET /draftcombinenonstationaryshooting`

Same parameters as `draftcombinestats`.

```bash
curl "https://stats.nba.com/stats/draftcombinenonstationaryshooting?LeagueID=00&SeasonYear=2024-25" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

---

## Draft Board

**PARTIALLY VERIFIED** — Live draft board with player rankings and availability status.

**Endpoint:** `GET /draftboard`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `LeagueID` | ✅ | `00` | `00` |
| `Season` | ✅ | Draft year in 4-digit format | `2024` |
| `RoundNum` | ❌ | Round filter | `` |
| `TopX` | ❌ | Top N picks | `` |

```bash
curl "https://stats.nba.com/stats/draftboard?LeagueID=00&Season=2024" \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

> **Note:** Best used before or during draft night. May return limited data post-draft.
