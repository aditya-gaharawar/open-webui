## 2024-05-22 - [CRITICAL] Unrestricted Signup Endpoint
**Vulnerability:** The signup endpoint (`/signup`) in `backend/answer_ai/routers/auths.py` had no rate limiting, allowing for mass account creation and potential denial of service.
**Learning:** Even if `signin` is protected, `signup` is often overlooked but critical for preventing abuse. Rate limiting by IP is essential here since there's no user identity yet.
**Prevention:** Always apply rate limiting to public-facing endpoints that modify state or trigger expensive operations, especially authentication-related ones.
