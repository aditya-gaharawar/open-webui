## 2025-05-27 - Missing Rate Limiting on Signup

**Vulnerability:** The `/signup` endpoint in `backend/answer_ai/routers/auths.py` lacked rate limiting, allowing an attacker to flood the database with new user accounts or enumerate internal behaviors.

**Learning:** Rate limiting is critical for unauthenticated endpoints, especially those that create resources (like user accounts). The existing `signin` endpoint had rate limiting, but `signup` was overlooked.

**Prevention:** Always verify that public endpoints, especially those involving resource creation or authentication, have appropriate rate limiting controls. Use the `RateLimiter` class consistently across all auth endpoints.
