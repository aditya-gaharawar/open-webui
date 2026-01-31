## 2024-05-23 - [CRITICAL] Missing Rate Limiting on Signup Endpoint
**Vulnerability:** The `/signup` endpoint lacked rate limiting, allowing a single IP address to create unlimited accounts, potentially leading to denial of service (DoS) and resource exhaustion.
**Learning:** While the `/signin` endpoint was protected, the `/signup` endpoint was overlooked. Critical resource-creation endpoints must always be rate-limited to prevent abuse.
**Prevention:** Always audit public endpoints (especially those creating resources like users) for rate limiting. Use shared rate limiter logic where applicable or define specific limits for sensitive actions.
