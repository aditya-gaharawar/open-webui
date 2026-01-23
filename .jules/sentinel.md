## 2025-05-27 - Unsafe Configuration Defaults
**Vulnerability:** Security headers (and potentially other configs) were only set if the corresponding environment variable was present. If missing, the app defaulted to insecure behavior (no headers).
**Learning:** The configuration pattern `value = os.environ.get(VAR); if value: set_config(value)` implicitly defaults to "nothing/unsafe" when the variable is missing. Secure defaults should be enforced in code, allowing environment variables to override them, not enable them.
**Prevention:** Use `os.environ.get(VAR, SAFE_DEFAULT)` or verify that `if not value:` sets a safe default. In `security_headers.py`, I changed the logic to pre-populate safe defaults and then update with env vars if present.
