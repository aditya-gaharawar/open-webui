import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os

from answerai.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MAIN"])

####################
# SMTP Configuration
####################

# Get SMTP settings from environment variables
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", "")
SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "AnswerAI")
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"
SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "false").lower() == "true"

# Email verification settings
EMAIL_VERIFICATION_ENABLED = (
    os.environ.get("EMAIL_VERIFICATION_ENABLED", "false").lower() == "true"
)
EMAIL_VERIFICATION_URL = os.environ.get("EMAIL_VERIFICATION_URL", "http://localhost:8080/auth/verify")
EMAIL_VERIFICATION_TOKEN_EXPIRY = int(
    os.environ.get("EMAIL_VERIFICATION_TOKEN_EXPIRY", "86400")  # 24 hours default
)


def is_email_configured() -> bool:
    """Check if email/SMTP is properly configured"""
    required_settings = [SMTP_HOST, SMTP_PORT, SMTP_FROM_EMAIL]
    return all(required_settings) and EMAIL_VERIFICATION_ENABLED


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
) -> tuple[bool, Optional[str]]:
    """
    Send an email using SMTP.
    Returns (success, error_message)
    """
    if not is_email_configured():
        log.warning("Email is not configured. Skipping email send.")
        return False, "Email is not configured"

    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        message["To"] = to_email

        # Add text and HTML parts
        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)

        part2 = MIMEText(html_content, "html")
        message.attach(part2)

        # Connect to SMTP server and send email
        if SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)

        if SMTP_USE_TLS and not SMTP_USE_SSL:
            server.starttls()

        # Login if credentials are provided
        if SMTP_USERNAME and SMTP_PASSWORD:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Send email
        server.send_message(message)
        server.quit()

        log.info(f"Email sent successfully to {to_email}")
        return True, None

    except Exception as e:
        log.error(f"Failed to send email to {to_email}: {str(e)}")
        return False, str(e)


def get_verification_email_template(
    user_name: str, verification_link: str, token_expiry_hours: int = 24
) -> tuple[str, str]:
    """
    Get the HTML and text templates for verification email.
    Returns (html_content, text_content)
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verify Your Email</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 40px;
                margin: 20px 0;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #2563eb;
                margin: 0;
                font-size: 28px;
            }}
            .content {{
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                padding: 14px 32px;
                background-color: #2563eb;
                color: #ffffff;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                text-align: center;
                margin: 20px 0;
            }}
            .button:hover {{
                background-color: #1d4ed8;
            }}
            .link {{
                word-break: break-all;
                color: #2563eb;
                font-size: 14px;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e5e7eb;
                font-size: 14px;
                color: #6b7280;
                text-align: center;
            }}
            .warning {{
                background-color: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 12px;
                margin: 20px 0;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Verify Your Email Address</h1>
            </div>
            
            <div class="content">
                <p>Hello {user_name},</p>
                
                <p>Thank you for signing up! To complete your registration and start using your account, please verify your email address by clicking the button below:</p>
                
                <div style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Email Address</a>
                </div>
                
                <p>Or copy and paste this link into your browser:</p>
                <p class="link">{verification_link}</p>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong> This verification link will expire in {token_expiry_hours} hours.
                </div>
                
                <p>If you didn't create an account, you can safely ignore this email.</p>
            </div>
            
            <div class="footer">
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; {SMTP_FROM_NAME}. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Verify Your Email Address
    
    Hello {user_name},
    
    Thank you for signing up! To complete your registration and start using your account, please verify your email address by clicking the link below:
    
    {verification_link}
    
    This verification link will expire in {token_expiry_hours} hours.
    
    If you didn't create an account, you can safely ignore this email.
    
    ---
    This is an automated message, please do not reply to this email.
    © {SMTP_FROM_NAME}. All rights reserved.
    """

    return html_content, text_content


def send_verification_email(
    to_email: str, user_name: str, verification_token: str, base_url: str
) -> tuple[bool, Optional[str]]:
    """
    Send a verification email to the user.
    Returns (success, error_message)
    """
    # Construct verification link
    verification_link = f"{base_url}?token={verification_token}"

    # Calculate token expiry in hours
    token_expiry_hours = EMAIL_VERIFICATION_TOKEN_EXPIRY // 3600

    # Get email templates
    html_content, text_content = get_verification_email_template(
        user_name, verification_link, token_expiry_hours
    )

    # Send email
    return send_email(
        to_email=to_email,
        subject="Verify Your Email Address",
        html_content=html_content,
        text_content=text_content,
    )


def send_welcome_email(to_email: str, user_name: str) -> tuple[bool, Optional[str]]:
    """
    Send a welcome email after successful verification.
    Returns (success, error_message)
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome!</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 40px;
                margin: 20px 0;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #10b981;
                margin: 0;
                font-size: 28px;
            }}
            .success-icon {{
                font-size: 48px;
                text-align: center;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">✓</div>
            <div class="header">
                <h1>Email Verified Successfully!</h1>
            </div>
            <div class="content">
                <p>Hello {user_name},</p>
                <p>Your email address has been successfully verified. You can now enjoy full access to your account.</p>
                <p>Thank you for joining us!</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Email Verified Successfully!
    
    Hello {user_name},
    
    Your email address has been successfully verified. You can now enjoy full access to your account.
    
    Thank you for joining us!
    """

    return send_email(
        to_email=to_email,
        subject="Welcome! Your Email is Verified",
        html_content=html_content,
        text_content=text_content,
    )
