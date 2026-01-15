## 2025-02-17 - Authentication Rate Limiting Patterns
**Vulnerability:** The `signup` endpoint lacked rate limiting, allowing account creation spam. The `signin` endpoint was rate-limited only by email, allowing credential stuffing attacks.
**Learning:** Backend integration tests are heavily dependent on Docker, making isolated unit testing of routers difficult due to global imports (e.g., `answer_ai.internal.db`). Mocking `sys.modules` is a necessary pattern to test these components in isolation.
**Prevention:** Always implement dual-layer rate limiting (IP-based + User/Resource-based) for sensitive endpoints. Use `sys.modules` mocking for testing legacy/tightly-coupled codebases.
