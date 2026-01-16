## 2025-05-22 - Missing SSRF Protection Implementation
**Vulnerability:** The memory and documentation claimed SSRF protection via `SafeAiohttpTCPConnector` existed, but the code was missing the connector implementation in `SafeWebBaseLoader`, leaving the application vulnerable to DNS rebinding attacks.
**Learning:** Documentation and memory can drift from codebase reality. Always verify security controls exist in the actual code, not just in descriptions.
**Prevention:** Implement automated tests that specifically attempt SSRF/DNS rebinding to verify the control is active.
