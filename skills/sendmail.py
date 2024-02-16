import smtplib
import os
def sendEmail(to, password, content):
    """Send an email using your credentials."""
    # Replace with your email and password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    email_id = os.environ.get("EMAIL_ID")
    email_password = password
    server.login(email_id, email_password)
    server.sendmail(email_id, to, content)
    server.close()
    return"Your message has been sent through the ether!"