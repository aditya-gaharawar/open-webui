## 2025-05-15 - Missing Rate Limiting on Signup
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing unlimited account creation attempts from a single IP address.
**Learning:** While `signin` had rate limiting, `signup` was overlooked. Rate limiting should be applied to all public-facing write endpoints, especially those creating resources or sending emails.
**Prevention:** Audit all public endpoints for rate limiting. Use a shared rate limiting utility (like `RateLimiter` class) and enforce it by default or via middleware if possible.
