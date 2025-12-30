## 2024-05-24 - RCE in Plugin Architecture
**Vulnerability:** The plugin system (`backend/answer_ai/utils/plugin.py`) uses `exec()` to run Python code stored in the database as Tools/Functions, and `subprocess.check_call` to install dependencies from user-supplied frontmatter.
**Learning:** This design effectively allows Remote Code Execution (RCE) as a feature. While access is restricted to admins (mostly), any compromise of an admin account or a vulnerability allowing non-admins to create/update tools leads to full server compromise. The `subprocess.check_call` usage with unsanitized input allows argument injection.
**Prevention:**
1. Avoid `exec()` and `eval()` on user-supplied code. Use sandboxed environments (e.g., Docker containers, WebAssembly, specialized sandboxes like PyPy sandbox or RestrictedPython) to execute untrusted code.
2. For dependency installation, parse requirements strictly (e.g., regex for valid package names/versions) before passing to `pip`, or better yet, pre-install allowed packages in the environment.
3. Validate all inputs to `subprocess` calls.
