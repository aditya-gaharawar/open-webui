## 2025-10-27 - Rate Limiting Missing on Signup
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing attackers to spam account creation (DoS/Database spam).
**Learning:** Publicly accessible endpoints that create resources (like users) MUST have rate limiting keyed by IP address to prevent abuse.
**Prevention:** Instantiated a `RateLimiter` keyed by IP (`request.client.host`) for the signup endpoint.
