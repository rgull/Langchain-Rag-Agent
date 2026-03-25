import os
from config.settings import settings

import smtplib
from email.message import EmailMessage

from langchain.tools import tool

@tool
def send_email_tool(recipient: str, subject: str, body: str):
    """
    Send an email to a specified recipient using SMTP.

    Required environment variables:
    - SMTP_HOST
    - SMTP_PORT (optional, default: 587)
    - SMTP_USERNAME
    - SMTP_PASSWORD
    - SMTP_SENDER_EMAIL (optional, defaults to SMTP_USERNAME)
    """
    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD
    sender_email = settings.SMTP_SENDER_EMAIL or smtp_username

    missing = [
        name
        for name, value in {
            "SMTP_HOST": smtp_host,
            "SMTP_USERNAME": smtp_username,
            "SMTP_PASSWORD": smtp_password,
        }.items()
        if not value
    ]
    if missing:
        return (
            "Email not sent. Missing required environment variables: "
            + ", ".join(missing)
        )

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        return f"Email sent successfully to {recipient}."
    except Exception as e:
        return f"Failed to send email to {recipient}. Error: {str(e)}"

@tool
def read_email_tool(email_id: str):
    """
    Read an email by its ID.
    """
    return f"Reading email with ID: {email_id}."