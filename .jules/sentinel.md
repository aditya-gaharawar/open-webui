## 2024-05-23 - [Missing Rate Limiting on LDAP Auth]
**Vulnerability:** The `/api/v1/auths/ldap` endpoint lacked rate limiting, while the standard `/signin` endpoint was protected. This allowed potential brute-force attacks against LDAP credentials.
**Learning:** When multiple authentication methods exist (local, LDAP, OAuth), ensure security controls like rate limiting are applied consistently across ALL of them. A gap in one is a gap in all.
**Prevention:** Audit all authentication endpoints for consistent application of security middleware and checks. Use shared or consistent rate limiters for all login paths.
