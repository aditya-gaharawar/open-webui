# 📧 Email Verification System for OpenWebUI

## ✨ Quick Start

### 1. Configure Environment Variables

Add to your `.env` file:

```bash
# Enable email verification
EMAIL_VERIFICATION_ENABLED=true

# SMTP Settings (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=AnswerAI
SMTP_USE_TLS=true

# Verification URL
EMAIL_VERIFICATION_URL=http://localhost:8080/auth/verify
EMAIL_VERIFICATION_TOKEN_EXPIRY=86400
```

### 2. Test SMTP Configuration

```bash
cd /workspace
python test_email_verification.py
```

### 3. Run the Application

```bash
cd backend
python -m answerai.main
```

## 📋 Features

✅ Secure email verification tokens  
✅ Professional HTML email templates  
✅ Token expiration (24 hours default)  
✅ One-time use tokens  
✅ Resend verification emails  
✅ Admin bypass  
✅ SMTP support (Gmail, SendGrid, AWS SES, etc.)  
✅ Complete API endpoints  
✅ Database migration included  
✅ Production-ready

## 🔌 API Endpoints

| Endpoint                              | Method | Description               |
| ------------------------------------- | ------ | ------------------------- |
| `/api/v1/email-verification/verify`   | POST   | Verify email with token   |
| `/api/v1/email-verification/resend`   | POST   | Resend verification email |
| `/api/v1/email-verification/status`   | GET    | Get verification status   |
| `/api/v1/email-verification/required` | GET    | Check if required         |

## 🔧 SMTP Providers

### Gmail

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Generate at https://myaccount.google.com/apppasswords
```

### SendGrid

```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

### AWS SES

```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your-aws-access-key-id
SMTP_PASSWORD=your-aws-secret-access-key
```

### Mailgun

```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=postmaster@yourdomain.com
SMTP_PASSWORD=your-mailgun-password
```

## 🔒 Security Features

- Cryptographically secure token generation
- Token expiration enforcement
- One-time use validation
- Admin user bypass
- Email format validation
- Rate limiting ready

## 📝 User Flow

1. **Signup** → User creates account with email
2. **Email Sent** → Verification email sent automatically
3. **User Clicks Link** → Token validated
4. **Email Verified** → User can now login
5. **Login Blocked** → Until email is verified (except admins)

## 🧪 Testing

```bash
# Test SMTP configuration
python test_email_verification.py

# Check if system is working
curl http://localhost:8080/api/v1/email-verification/required

# Resend verification email
curl -X POST http://localhost:8080/api/v1/email-verification/resend \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

## 📂 Files Added/Modified

### New Files

- `backend/answerai/models/email_verification.py` - Database models
- `backend/answerai/utils/email.py` - Email utilities and templates
- `backend/answerai/routers/email_verification.py` - API endpoints
- `backend/answerai/migrations/versions/add_email_verification.py` - Database migration
- `test_email_verification.py` - SMTP testing script

### Modified Files

- `backend/answerai/models/users.py` - Added `email_verified` field
- `backend/answerai/models/auths.py` - Updated signup to support verification
- `backend/answerai/routers/auths.py` - Integrated email verification flow
- `backend/answerai/main.py` - Registered email verification router

## 🐛 Troubleshooting

### Emails Not Sending?

1. Check SMTP credentials
2. For Gmail, use App Password (not regular password)
3. Check firewall/port access
4. Review logs: `docker logs answerai-backend`
5. Run test script: `python test_email_verification.py`

### Login Blocked?

1. Check if email is verified:
   ```sql
   SELECT email, email_verified FROM user WHERE email='user@example.com';
   ```
2. Manually verify (emergency):
   ```sql
   UPDATE user SET email_verified=1 WHERE email='user@example.com';
   ```

## 📚 Full Documentation

See `EMAIL_VERIFICATION_SETUP.md` for complete documentation including:

- Detailed setup instructions
- Frontend integration examples
- Production recommendations
- Customization guide
- Advanced troubleshooting

## 🚀 Production Checklist

- [ ] Set `EMAIL_VERIFICATION_ENABLED=true`
- [ ] Configure production SMTP server
- [ ] Update `EMAIL_VERIFICATION_URL` to production domain
- [ ] Test email sending
- [ ] Monitor verification rates
- [ ] Set up email delivery monitoring
- [ ] Configure rate limiting
- [ ] Set up automated token cleanup

## 💡 Tips

- **First Admin**: Automatically verified (no email needed)
- **Disable**: Set `EMAIL_VERIFICATION_ENABLED=false` to disable
- **Testing**: Use Mailtrap.io or MailHog for local testing
- **Resend**: Users can request new verification emails
- **Expiry**: Default 24h, configurable via `EMAIL_VERIFICATION_TOKEN_EXPIRY`

## 📄 License

Part of OpenWebUI - Same license applies

---

**Need Help?** Check `EMAIL_VERIFICATION_SETUP.md` for detailed documentation
