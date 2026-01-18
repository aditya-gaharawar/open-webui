## 2024-05-23 - Missing Signup Rate Limiting
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing for potential account creation spam and DoS.
**Learning:** Developers often prioritize securing `/signin` (brute force protection) but overlook `/signup` (spam protection), assuming user creation is a lower frequency event or less risky.
**Prevention:** Apply rate limiting to ALL public unauthenticated endpoints by default, or implement a global rate limiter middleware.
