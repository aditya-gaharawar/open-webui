## 2025-02-18 - Missing Signup Rate Limiting
**Vulnerability:** The `/signup` endpoint was completely unprotected against automated abuse, allowing unlimited account creation from a single IP.
**Learning:** While `signin` was protected, `signup` was overlooked. This highlights the importance of auditing all public write endpoints, not just authentication verification ones.
**Prevention:** Ensure all public-facing endpoints that create resources (users, etc.) have rate limiting applied using the project's `RateLimiter` utility.
