# Email Verification System - Setup Guide

## Overview

This is a production-grade email verification system for OpenWebUI (AnswerAI). It provides complete end-to-end email verification functionality with SMTP support.

## Features

✅ **Email Verification System**
- Email verification tokens with secure random generation
- Token expiration (configurable, default 24 hours)
- Token usage tracking (one-time use)
- Automatic email sending on signup

✅ **SMTP Email Support**
- Configurable SMTP server settings
- TLS/SSL support
- HTML email templates with responsive design
- Text fallback for email clients that don't support HTML

✅ **API Endpoints**
- `POST /api/v1/email-verification/verify` - Verify email with token
- `POST /api/v1/email-verification/resend` - Resend verification email
- `GET /api/v1/email-verification/status` - Get verification status
- `GET /api/v1/email-verification/required` - Check if verification is required

✅ **Security Features**
- Secure token generation using `secrets.token_urlsafe()`
- Token expiration with configurable time
- One-time use tokens
- Admin users bypass email verification
- Email verification can be enabled/disabled

✅ **Database Models**
- Added `email_verified` field to User table
- New `email_verification_token` table with indexes
- Database migration included

## Setup Instructions

### 1. Environment Configuration

Create or update your `.env` file with the following settings:

```bash
# Enable email verification
EMAIL_VERIFICATION_ENABLED=true

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=AnswerAI
SMTP_USE_TLS=true
SMTP_USE_SSL=false

# Email verification URL (your frontend URL)
EMAIL_VERIFICATION_URL=http://localhost:8080/auth/verify

# Token expiry (24 hours = 86400 seconds)
EMAIL_VERIFICATION_TOKEN_EXPIRY=86400
```

### 2. SMTP Setup Examples

#### Gmail Setup
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in `SMTP_PASSWORD`

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=true
```

#### SendGrid Setup
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_USE_TLS=true
```

#### AWS SES Setup
```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your-aws-access-key-id
SMTP_PASSWORD=your-aws-secret-access-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_USE_TLS=true
```

#### Mailgun Setup
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=postmaster@yourdomain.com
SMTP_PASSWORD=your-mailgun-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_USE_TLS=true
```

### 3. Database Migration

The database migration will be automatically run when you start the application. It will:
- Add `email_verified` column to the `user` table
- Create the `email_verification_token` table
- Add necessary indexes for performance

To manually run migrations:
```bash
cd backend
alembic upgrade head
```

### 4. Start the Application

```bash
cd backend
python -m answerai.main
```

Or if using Docker:
```bash
docker-compose up -d
```

## How It Works

### User Signup Flow

1. **User Signs Up**
   - User fills out signup form with name, email, and password
   - If email verification is enabled, user is created with `email_verified=False`
   - A verification token is generated and stored in the database
   - Verification email is sent to the user's email address

2. **User Receives Email**
   - Email contains a verification link: `{EMAIL_VERIFICATION_URL}?token={token}`
   - Link is valid for 24 hours (configurable)
   - Email template is responsive and looks professional

3. **User Clicks Verification Link**
   - Frontend captures the token from URL
   - Frontend calls `POST /api/v1/email-verification/verify` with the token
   - Backend verifies token validity and marks email as verified
   - Token is marked as used (one-time use)
   - User receives a welcome email (optional)

4. **User Logs In**
   - If email is not verified, login is blocked with appropriate error message
   - Admin users bypass email verification
   - After verification, user can log in normally

### Special Cases

- **First Admin User**: Automatically verified (no email verification needed)
- **OAuth Users**: Email verification can be skipped for OAuth signups
- **Admin Users**: Can always login regardless of email verification status
- **LDAP Users**: Can configure email verification separately

## API Documentation

### Verify Email
```http
POST /api/v1/email-verification/verify
Content-Type: application/json

{
  "token": "verification_token_here"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email verified successfully",
  "email_verified": true
}
```

### Resend Verification Email
```http
POST /api/v1/email-verification/resend
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Verification email has been sent"
}
```

### Check Verification Status
```http
GET /api/v1/email-verification/status
Authorization: Bearer {token}
```

**Response:**
```json
{
  "enabled": true,
  "email_verified": false
}
```

### Check if Verification Required
```http
GET /api/v1/email-verification/required
```

**Response:**
```json
{
  "required": true,
  "configured": true
}
```

## Frontend Integration

### Verification Page Example

Create a page at `/auth/verify` in your frontend:

```typescript
// Example using SvelteKit
import { onMount } from 'svelte';

let token = '';
let status = 'pending'; // pending, success, error
let message = '';

onMount(async () => {
  // Get token from URL
  const params = new URLSearchParams(window.location.search);
  token = params.get('token') || '';
  
  if (token) {
    try {
      const response = await fetch('/api/v1/email-verification/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        status = 'success';
        message = data.message;
        // Redirect to login after 3 seconds
        setTimeout(() => {
          window.location.href = '/auth';
        }, 3000);
      } else {
        status = 'error';
        message = data.detail || 'Verification failed';
      }
    } catch (error) {
      status = 'error';
      message = 'An error occurred during verification';
    }
  }
});
```

### Resend Verification Email Example

```typescript
async function resendVerification(email: string) {
  try {
    const response = await fetch('/api/v1/email-verification/resend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert(data.message);
    } else {
      alert(data.detail || 'Failed to resend email');
    }
  } catch (error) {
    alert('An error occurred');
  }
}
```

## Email Templates

The system includes professional HTML email templates:

### Verification Email
- Clean, modern design
- Responsive layout
- Clear call-to-action button
- Fallback plain text link
- Expiration warning
- Mobile-friendly

### Welcome Email
- Sent after successful verification
- Confirmation message
- Professional design

## Testing

### Local Testing (Development)

For local testing, you can use a test SMTP service like:

1. **Mailtrap** (https://mailtrap.io)
   - Free tier available
   - Perfect for testing
   ```bash
   SMTP_HOST=sandbox.smtp.mailtrap.io
   SMTP_PORT=2525
   SMTP_USERNAME=your-mailtrap-username
   SMTP_PASSWORD=your-mailtrap-password
   ```

2. **MailHog** (Docker)
   ```bash
   docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
   
   SMTP_HOST=localhost
   SMTP_PORT=1025
   SMTP_USE_TLS=false
   ```

### Testing Checklist

- [ ] User signup creates unverified user
- [ ] Verification email is sent
- [ ] Token verification works correctly
- [ ] Expired tokens are rejected
- [ ] Used tokens are rejected
- [ ] Invalid tokens are rejected
- [ ] Resend email works
- [ ] Login is blocked for unverified users
- [ ] Admin users can login without verification
- [ ] Welcome email is sent after verification

## Troubleshooting

### Email Not Sending

1. **Check SMTP credentials**
   - Verify username and password are correct
   - For Gmail, ensure you're using an App Password

2. **Check firewall/network**
   - Ensure port 587 (or 465 for SSL) is not blocked
   - Try pinging the SMTP server

3. **Check logs**
   ```bash
   docker logs answerai-backend
   ```

4. **Test SMTP connection**
   ```python
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email', 'your-password')
   server.quit()
   ```

### Verification Not Working

1. **Check if email verification is enabled**
   - `EMAIL_VERIFICATION_ENABLED=true`

2. **Check token expiration**
   - Default is 24 hours
   - Increase `EMAIL_VERIFICATION_TOKEN_EXPIRY` if needed

3. **Check database**
   - Verify token exists in `email_verification_token` table
   - Check `used` and `expires_at` columns

### User Can't Login

1. **Check email verification status**
   ```sql
   SELECT id, email, email_verified FROM user WHERE email = 'user@example.com';
   ```

2. **Manually verify user (emergency)**
   ```sql
   UPDATE user SET email_verified = 1 WHERE email = 'user@example.com';
   ```

## Production Recommendations

### Security

1. **Use environment variables** - Never hardcode SMTP credentials
2. **Enable TLS** - Always use encrypted connections
3. **Rate limiting** - Limit verification email resend attempts
4. **Token expiration** - Keep default 24 hours or less
5. **Monitor logs** - Watch for verification failures

### Performance

1. **Background tasks** - Send emails asynchronously
2. **Cleanup job** - Periodically delete expired tokens
3. **Email queue** - Use message queue for high volume
4. **Database indexes** - Migration includes optimized indexes

### Monitoring

1. **Track verification rates** - Monitor successful verifications
2. **Email delivery** - Monitor email sending success
3. **Token expiration** - Track expired tokens
4. **Failed verifications** - Alert on high failure rates

## Customization

### Email Templates

Edit the templates in `backend/answerai/utils/email.py`:
- `get_verification_email_template()` - Main verification email
- `send_welcome_email()` - Welcome email after verification

### Verification Logic

Edit `backend/answerai/routers/email_verification.py`:
- Add custom verification rules
- Modify expiration logic
- Add additional email types

### Token Generation

Edit `backend/answerai/models/email_verification.py`:
- Modify token length
- Change expiration handling
- Add custom token validation

## Support

For issues or questions:
1. Check the logs: `docker logs answerai-backend`
2. Review this documentation
3. Check environment variables are set correctly
4. Test SMTP connection separately
5. Review the code in `backend/answerai/routers/email_verification.py`

## License

This email verification system is part of OpenWebUI and follows the same license.
