## 2026-01-24 - [Signup Rate Limiting]
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing potential DoS or account creation spam.
**Learning:** `auths.py` had rate limiting for `signin` but not `signup`.
**Prevention:** Always audit public endpoints (especially creation endpoints) for rate limiting. Added 5 req/hour limit per IP for signup.
