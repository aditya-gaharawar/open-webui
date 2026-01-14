## 2025-02-18 - Missing Rate Limiting on Signup Endpoint
**Vulnerability:** The `/signup` endpoint in `backend/answer_ai/routers/auths.py` lacks rate limiting, allowing an attacker to create an unlimited number of accounts, potentially leading to database exhaustion or denial of service.
**Learning:** Authentication endpoints are high-value targets. While `signin` was protected, `signup` was overlooked. Consistent application of security controls across all authentication-related endpoints is crucial.
**Prevention:** Ensure all public-facing endpoints that modify state or consume significant resources (like account creation) have appropriate rate limiting applied. Use a centralized configuration for rate limits where possible.
