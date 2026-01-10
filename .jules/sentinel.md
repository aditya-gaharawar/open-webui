## 2024-05-23 - [CORS Configuration]
**Vulnerability:** The default CORS configuration allows all origins (`*`), which permits any website to make requests to the backend API.
**Learning:** Even though the config file has a warning, the default behavior is insecure out of the box. This is common in "developer-friendly" setups but dangerous for production.
**Prevention:** Change the default to a safe value (like `localhost` or empty) and force users to explicitly allow external origins.
