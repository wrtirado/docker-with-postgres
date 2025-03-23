# Description: Service to send email via SendGrid.
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")


def send_email(email: str, auth_code: str):
    """Send authentication code via SendGrid."""
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=email,
        subject="Your Authentication Code",
        plain_text_content=f"Your login code is: {auth_code}",
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {email}: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
