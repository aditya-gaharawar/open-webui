## 2026-01-14 - [Missing Rate Limiting on Signup]
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing potential DoS or bulk account creation attacks.
**Learning:** While `signin` was protected, `signup` was not. Rate limiting should be applied to all public authentication endpoints. The project uses a custom `RateLimiter` class with Redis/Memory fallback.
**Prevention:** Audit all public `POST` endpoints in `routers/` for `RateLimiter` usage.
