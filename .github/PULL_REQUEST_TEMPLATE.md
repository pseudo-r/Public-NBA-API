## Summary

<!-- What does this PR do? -->

## Type of Change

- [ ] 📝 Documentation fix (incorrect endpoint, wrong parameters, typo)
- [ ] 🔍 New endpoint documented
- [ ] 🐛 Bug fix in `nba_service/`
- [ ] ✨ New feature in `nba_service/`
- [ ] 🔧 Chore / maintenance

## Checklist

- [ ] I have tested any endpoint URLs I'm adding/correcting (include the curl command and response snippet)
- [ ] Markdown renders correctly (headers, tables, code blocks)
- [ ] Follows the existing doc style (endpoint-first, example-driven)
- [ ] If adding `nba_service` changes: tests pass (`docker compose exec web pytest`)

## Endpoint Verification (if applicable)

```bash
curl "https://stats.nba.com/stats/..." \
  -H "Referer: https://www.nba.com/" \
  -H "x-nba-stats-origin: stats" \
  -H "x-nba-stats-token: true"
```

**Status code:**
**Response excerpt:**
```json

```

## Related Issues

Closes #
