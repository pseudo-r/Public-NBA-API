# Contributing

Adding new endpoints, correcting parameters, or fixing examples is welcome.

---

## How to Contribute

### Found a new endpoint?

1. Open an issue or PR describing:
   - The full URL
   - All required and optional parameters
   - A `curl` or Python example
   - The `resultSets` names and column headers
   - Whether the endpoint is VERIFIED, PARTIALLY VERIFIED, or UNVERIFIED

### Fixing an existing endpoint?

1. If parameters changed or a response structure is stale, update the relevant file under `docs/`
2. Update `CHANGELOG.md` with a note about what changed

---

## Verification Levels

| Label | Meaning |
|-------|---------|
| **VERIFIED** | Tested live against the real API with observed response |
| **PARTIALLY VERIFIED** | URL confirmed working, but not all parameters fully tested |
| **UNVERIFIED** | Known from source references but not personally tested |

All new endpoints should include an honest verification label.

---

## Documentation Style

Match the existing style:
- Lead with the endpoint URL and verification label
- Use a parameter table (Required / Optional clearly marked)
- Include a `curl` or Python example that can be copy-pasted
- Include column headers for key `resultSets`
- Add notes for gotchas (empty responses, format differences, singular `resultSet`, etc.)

Do **not** add speculative information. If you're unsure, say so.

---

## Adding Headers

The required NBA Stats API headers belong in the main [README.md](README.md). Only mention them in individual endpoint docs if an endpoint has different requirements.
