## 2025-02-18 - Missing Rate Limiting on Signup Endpoint

**Vulnerability:** The `/signup` endpoint in `backend/answer_ai/routers/auths.py` was completely unprotected by rate limiting, allowing mass account creation attacks. While `/signin` had a rate limiter, `/signup` did not.

**Learning:** Rate limiting logic was inconsistently applied. The application relies on `request.client.host` for IP-based limiting, which requires careful handling of internal/trusted calls (e.g. from upstream auth proxies) to avoid blocking legitimate bulk operations or internal provisioning.

**Prevention:** Ensure all public-facing authentication and resource creation endpoints have explicit rate limiting. Use shared utility classes like `RateLimiter` consistently. When implementing "trusted header" authentication, verify that rate limiting policies align with the assumption that the upstream proxy handles DoS protection.
