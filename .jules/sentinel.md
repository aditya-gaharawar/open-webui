## 2026-01-25 - Rate Limiting Missing on Signup
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing unlimited account creation from a single IP address.
**Learning:** While `signin` was protected, `signup` was not. This inconsistency highlights the need to audit all authentication endpoints for rate limiting.
**Prevention:** Ensure all public endpoints that trigger resource creation or authentication have appropriate rate limiting configured.
