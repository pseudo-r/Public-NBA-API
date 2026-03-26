---
name: "🐛 Bug Report"
about: "Report a broken or incorrect API endpoint"
title: "[BUG] "
labels: ["bug"]
assignees: []
---

## Endpoint

<!-- The full URL you were trying to use -->
```
GET https://stats.nba.com/stats/...
```

## Expected Behavior

<!-- What did you expect to get back? -->

## Actual Behavior

<!-- What did you actually get? Include status code and response snippet -->

**Status code:**
**Response:**
```json

```

## Steps to Reproduce

```bash
curl "https://stats.nba.com/stats/..." \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

## Environment

- Date tested:
- Endpoint:
- Any query params used:
