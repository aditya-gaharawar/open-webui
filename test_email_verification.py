#!/usr/bin/env python3
"""
Test script for email verification system
This script helps test the SMTP configuration and email verification flow
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_connection():
    """Test SMTP connection with environment variables"""
    print("=" * 60)
    print("Testing SMTP Configuration")
    print("=" * 60)
    
    # Get SMTP settings
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", "")
    SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"
    SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "false").lower() == "true"
    
    print(f"\nSMTP Host: {SMTP_HOST}")
    print(f"SMTP Port: {SMTP_PORT}")
    print(f"SMTP Username: {SMTP_USERNAME}")
    print(f"SMTP From Email: {SMTP_FROM_EMAIL}")
    print(f"SMTP Use TLS: {SMTP_USE_TLS}")
    print(f"SMTP Use SSL: {SMTP_USE_SSL}")
    print(f"SMTP Password: {'*' * len(SMTP_PASSWORD) if SMTP_PASSWORD else '(not set)'}")
    
    # Check if all required settings are set
    if not all([SMTP_HOST, SMTP_PORT, SMTP_FROM_EMAIL]):
        print("\n❌ ERROR: Missing required SMTP configuration")
        print("Please set SMTP_HOST, SMTP_PORT, and SMTP_FROM_EMAIL environment variables")
        return False
    
    # Test connection
    print("\n📧 Testing SMTP connection...")
    try:
        if SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        
        if SMTP_USE_TLS and not SMTP_USE_SSL:
            server.starttls()
        
        if SMTP_USERNAME and SMTP_PASSWORD:
            print("🔐 Authenticating...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        server.quit()
        print("✅ SMTP connection successful!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check your username and password.")
        print("For Gmail, make sure you're using an App Password, not your regular password.")
        return False
    except smtplib.SMTPConnectError:
        print(f"❌ Could not connect to SMTP server {SMTP_HOST}:{SMTP_PORT}")
        print("Check if the host and port are correct and not blocked by firewall.")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def send_test_email(to_email: str):
    """Send a test email"""
    print("\n" + "=" * 60)
    print("Sending Test Email")
    print("=" * 60)
    
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", "")
    SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "AnswerAI")
    SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"
    SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "false").lower() == "true"
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Test Email from AnswerAI Email Verification System"
        message["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        message["To"] = to_email
        
        # HTML content
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Test Email</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 40px;">
                <h1 style="color: #2563eb; text-align: center;">✅ Test Email Successful!</h1>
                <p>This is a test email from the AnswerAI Email Verification System.</p>
                <p>If you received this email, your SMTP configuration is working correctly.</p>
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                <p style="font-size: 14px; color: #6b7280; text-align: center;">
                    This is an automated test message.
                </p>
            </div>
        </body>
        </html>
        """
        
        text_content = """
        Test Email Successful!
        
        This is a test email from the AnswerAI Email Verification System.
        
        If you received this email, your SMTP configuration is working correctly.
        
        ---
        This is an automated test message.
        """
        
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Connect and send
        print(f"\n📧 Sending test email to {to_email}...")
        
        if SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        
        if SMTP_USE_TLS and not SMTP_USE_SSL:
            server.starttls()
        
        if SMTP_USERNAME and SMTP_PASSWORD:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        server.send_message(message)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📬 Check {to_email} for the test email")
        return True
        
    except Exception as e:
        print(f"❌ Error sending test email: {str(e)}")
        return False


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("AnswerAI Email Verification System - Test Script")
    print("=" * 60)
    print("\nThis script tests your SMTP configuration for the email")
    print("verification system.")
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("\n📄 Loading environment variables from .env file...")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ Environment variables loaded")
        except ImportError:
            print("⚠️  python-dotenv not installed. Using system environment variables.")
    else:
        print("\n⚠️  No .env file found. Using system environment variables.")
    
    # Test SMTP connection
    if not test_smtp_connection():
        print("\n❌ SMTP connection test failed")
        print("\nPlease check your SMTP configuration in .env file:")
        print("  - SMTP_HOST")
        print("  - SMTP_PORT")
        print("  - SMTP_USERNAME")
        print("  - SMTP_PASSWORD")
        print("  - SMTP_FROM_EMAIL")
        sys.exit(1)
    
    # Ask if user wants to send test email
    print("\n" + "=" * 60)
    send_test = input("\nDo you want to send a test email? (y/n): ").lower().strip()
    
    if send_test == 'y':
        to_email = input("Enter recipient email address: ").strip()
        if to_email:
            send_test_email(to_email)
        else:
            print("❌ No email address provided")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
