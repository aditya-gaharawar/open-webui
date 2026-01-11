## 2026-01-11 - [Testing Config-Dependent Routers]
**Vulnerability:** N/A (Testing Challenge)
**Learning:** `backend/answer_ai/config.py` executes database queries and migrations immediately upon import. To test routers like `auths.py` that depend on `config.py` without a running database, one must patch `answer_ai.internal.db` in `sys.modules` *before* any other imports occur.
**Prevention:** Use extensive `sys.modules` mocking in pytest fixtures for unit tests involving config-heavy modules.
