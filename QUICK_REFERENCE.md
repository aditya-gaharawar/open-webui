# AnswerAI - Quick Reference Guide

## 🎯 What Changed?

Your codebase has been **completely white-labeled** from OpenWebUI to AnswerAI.

## 📋 Key Replacements

| Old                 | New                    |
| ------------------- | ---------------------- |
| `open_webui`        | `answer_ai`            |
| `openwebui`         | `answerai`             |
| `open-webui`        | `answer-ai`            |
| `Open WebUI`        | `AnswerAI`             |
| `WebUI`             | `AnswerAI`             |
| `WEBUI_*`           | `ANSWERAI_*`           |
| `webui.db`          | `answerai.db`          |
| `.webui_secret_key` | `.answerai_secret_key` |

## 🚀 Quick Start Commands

### Development

```bash
cd /workspace/project/answer-ai/backend
python -m answer_ai.main
```

### Testing

```bash
cd /workspace/project/answer-ai
pytest backend/answer_ai/test/
```

### Docker

```bash
cd /workspace/project/answer-ai
docker-compose up
```

## 📦 Package Information

**Package Name:** `answerai`  
**Python Module:** `answer_ai`  
**Main Entry:** `backend/answer_ai/main.py`

## 🔧 Environment Variables

Update your `.env` file with new variable names:

```bash
# Old → New
WEBUI_SECRET_KEY → ANSWERAI_SECRET_KEY
WEBUI_NAME → ANSWERAI_NAME
WEBUI_VERSION → ANSWERAI_VERSION
WEBUI_URL → ANSWERAI_URL
WEBUI_API_BASE_URL → ANSWERAI_API_BASE_URL
WEBUI_BASE_URL → ANSWERAI_BASE_URL
WEBUI_HOSTNAME → ANSWERAI_HOSTNAME
WEBUI_DEPLOYMENT_ID → ANSWERAI_DEPLOYMENT_ID
WEBUI_BUILD_HASH → ANSWERAI_BUILD_HASH
```

## 📁 File Locations

```
answer-ai/
├── backend/answer_ai/          # Main Python package (was: open_webui)
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration
│   ├── models/                 # Database models
│   ├── routers/                # API routes
│   └── test/apps/answerai/     # Tests (was: webui)
├── src/                        # Frontend (SvelteKit)
│   └── lib/constants.ts        # ANSWERAI_* constants
├── answerai.db                 # Database file (was: webui.db)
└── .answerai_secret_key        # Secret key (was: .webui_secret_key)
```

## 🔍 Verification

To verify all changes:

```bash
# Should return only 3 results (external Stable Diffusion service)
grep -ri "webui\|open_webui" \
  --include="*.py" --include="*.js" --include="*.ts" \
  --include="*.svelte" --include="*.json" \
  --exclude-dir=.git --exclude-dir=node_modules . \
  | grep -iv "stable-diffusion" | grep -v "WHITE_LABEL"
```

## 📚 Documentation

Read these files for complete details:

1. **FINAL_WHITELABEL_REPORT.md** - Comprehensive transformation guide
2. **FINAL_SESSION_CHANGES.md** - Latest session changes
3. **WHITE_LABEL_COMPLETE_REPORT.md** - Previous completion summary

## ⚠️ Migration Notes

If migrating from an existing OpenWebUI installation:

1. **Rename database file:**

   ```bash
   mv webui.db answerai.db
   ```

2. **Rename secret key:**

   ```bash
   mv .webui_secret_key .answerai_secret_key
   ```

3. **Update environment variables** in your `.env` or `docker-compose.yml`

4. **Update Python imports** in any custom code:

   ```python
   # Old
   from open_webui.models.users import Users

   # New
   from answer_ai.models.users import Users
   ```

## ✅ What's Preserved

- ✅ All functionality intact
- ✅ Same API endpoints
- ✅ Database schema compatible
- ✅ All features working
- ✅ All tests operational

## 🎉 Ready to Deploy!

Your AnswerAI instance is fully branded and ready for production use.

---

**Generated:** 2025-12-29  
**Status:** ✅ Complete  
**Version:** AnswerAI 1.0
