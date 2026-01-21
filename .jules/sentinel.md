## 2024-05-23 - [Rate Limiting Signup Endpoint]
**Vulnerability:** The `signup` endpoint in `backend/answer_ai/routers/auths.py` lacked rate limiting, allowing for potential account creation flooding and Denial of Service (DoS) attacks via expensive password hashing operations.
**Learning:** Rate limiting was implemented for `signin` using `RateLimiter` but was missing for `signup`. Rate limiting strategies must differ: `signin` limits by email (or IP), while `signup` must limit by IP since the email is new/untrusted.
**Prevention:** Ensure all public unauthenticated endpoints (signup, password reset, etc.) have appropriate rate limiting applied using the client's IP address.
