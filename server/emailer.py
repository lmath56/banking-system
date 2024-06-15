# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Emailer File

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import CONFIG


class EmailSendingError(Exception):
    """Custom exception raised when an error occurs during email sending."""
    def __init__(self, message, original_error=None):
        super().__init__(message)
        self.original_error = original_error
        

def send_email(receiver_email, subject, body):
    """Sends an email to the specified receiver email address."""
    sender_email = CONFIG["smtp"]["sender_email"]

    message = MIMEMultipart()
    message["From"] = f"{CONFIG['smtp']['sender_name']} <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(CONFIG["smtp"]["host"], CONFIG["smtp"]["port"], context=context) as server:
            server.login(CONFIG["smtp"]["username"], CONFIG["smtp"]["password"])
            server.sendmail(sender_email, receiver_email, text)
            from manager import event_logger
            event_logger(f"Email '{subject}' sent to {receiver_email}") # Log the message
    except Exception as e:
        error_message = f"Failed to send email to {receiver_email}: {e}"
        from manager import event_logger
        event_logger(error_message) # Log the error
        raise EmailSendingError(error_message)


if __name__ == "__main__":
    email = "l.mathews@student.fontys.nl"
    subject = "Test Email"
    body = "This is a test email."
    try:
        send_email(email, subject, body)
    except EmailSendingError:
        print("Email sending failed.")
