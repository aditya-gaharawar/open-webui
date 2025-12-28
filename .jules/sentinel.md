## 2025-02-18 - SSRF in Image Processing
**Vulnerability:** Found a critical Server-Side Request Forgery (SSRF) vulnerability in `backend/open_webui/routers/images.py`. The `get_image_data` and `load_url_image` functions were taking user-provided URLs and blindly fetching them using `requests.get` without any validation. This allows attackers to access internal network resources or localhost services (e.g. metadata services, internal admin panels).

**Learning:** The vulnerability existed because the developer assumed user input was safe or relied on `requests` to handle it safely (which it doesn't for SSRF). While the project had a `validate_url` utility in `retrieval/web/utils.py` that blocks private IPs, it wasn't being used in the image processing module. This highlights the importance of centralizing security controls and ensuring they are applied across all relevant endpoints.

**Prevention:** Always validate user-provided URLs against a strict allowlist or blocklist (blocking private IPs/localhost) before making any server-side HTTP requests. Use a centralized validation utility (like `validate_url`) consistently across the codebase.
