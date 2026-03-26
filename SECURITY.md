# Security Policy

## Supported Versions

This repository documents an **unofficial, public API** (`stats.nba.com`) that is not operated by us.

| Component | Supported |
|-----------|-----------|
| Documentation (`docs/`) | ✅ Actively maintained |
| Django service (`nba_service/`) | ✅ Latest release |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

If you discover a security issue in the `nba_service` Django application (e.g., a vulnerability in the API service itself, authentication bypass, or data exposure), please report it responsibly:

1. Open a **private security advisory** on GitHub: [Security tab → Advisories → New advisory](https://github.com/pseudo-r/Public-NBA-API/security/advisories/new)
2. Include:
   - A clear description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within **72 hours** and aim to release a patch within **7 days** for confirmed vulnerabilities.

## Scope

### In scope
- SQL injection or authentication bypass in `nba_service/`
- Exposed secrets or credentials in committed code
- Insecure default configurations in `docker-compose.yml` or `Dockerfile`

### Out of scope
- Vulnerabilities in `stats.nba.com` itself — this is the NBA's property; report to them directly
- Rate limiting or WAF behaviour on `stats.nba.com`
- Documentation errors (open a normal issue instead)

## Disclaimer

This project is not affiliated with or endorsed by the NBA. The `stats.nba.com` API is unofficial and undocumented. Use responsibly and in accordance with the NBA's Terms of Service.
