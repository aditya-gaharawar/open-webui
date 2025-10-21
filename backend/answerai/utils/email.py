import smtplib
from email.message import EmailMessage
from typing import Optional


def send_email_smtp(
    host: str,
    port: int,
    username: Optional[str],
    password: Optional[str],
    starttls: bool,
    from_email: str,
    from_name: Optional[str],
    to_email: str,
    subject: str,
    html_body: str,
    text_body: Optional[str] = None,
    reply_to: Optional[str] = None,
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
    msg["To"] = to_email
    if reply_to:
        msg["Reply-To"] = reply_to

    if text_body is None:
        # Generate a basic text fallback from HTML
        import re

        stripped = re.sub("<[^<]+?>", "", html_body)
        text_body = stripped

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(host=host, port=port, timeout=30) as server:
        if starttls:
            server.starttls()
        if username:
            server.login(username, password or "")
        server.send_message(msg)
