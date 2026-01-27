## 2024-05-23 - [CRITICAL] Signup Rate Limiting Gap
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing a potential denial-of-service or bulk account creation attack (spam/credential stuffing risk).
**Learning:** Even if `signin` is rate-limited, creating new accounts is an expensive operation and must also be throttled.
**Prevention:** Always apply rate limiting to public unauthenticated endpoints that write state or perform expensive ops.
