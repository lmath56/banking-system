# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Emailer

import smtplib, ssl
from config import CONFIG # Import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

context = ssl.create_default_context() # Create a secure SSL context

email = "l.mathews@student.fontys.nl" # These three lines are for testing purposes
subject = "Test Email"
body = "This is a test email."

def send_email(receiver_email, subject, body):
    """Sends an email to the specified receiver email address."""
    sender_email = CONFIG["smtp"]["sender_email"]

    message = MIMEMultipart() # Create a multipart message and set headers
    message["From"] = f"{CONFIG["smtp"]["sender_name"]} <{CONFIG["smtp"]["sender_email"]}>"
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain")) # Add body to email

    text = message.as_string()

    with smtplib.SMTP_SSL(CONFIG["smtp"]["host"], CONFIG["smtp"]["port"], context=context) as server:
        server.login(CONFIG["smtp"]["username"], CONFIG["smtp"]["password"])
        server.sendmail(sender_email, receiver_email, text)
        print(f"Email sent to {receiver_email}.")
        server.quit()

if __name__ == "__main__":
    send_email(email, subject, body)