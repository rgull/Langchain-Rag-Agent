from langchain.tools import tool

@tool
def send_email_tool(recipient: str, subject: str, body: str):
    """
    Send an email to a specified recipient.
    """
    return f"Email sent to {recipient} with subject '{subject}' and body '{body}'."

@tool
def read_email_tool(email_id: str):
    """
    Read an email by its ID.
    """
    return f"Reading email with ID: {email_id}."