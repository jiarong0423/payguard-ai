# Backend trust boundary

Owner: mainline. FastAPI implements the localhost-only session/CSRF proxy described in docs/decisions/2026Q4/console_contract.md. Secrets are supplied only through backend environment. No browser receives credentials. Bounded sessions, rate limits and safe error responses are required before acceptance. No financial submission or production deployment.
