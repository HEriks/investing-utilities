import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

import report_scraper

def get_email_credentials(file):
    f = open(file, "r")
    email = f.readline()
    pwd = f.readline()
    return email, pwd

def get_receiver_email(file):
    f = open(file, "r")
    return f.readline()


def main():
    # Email setup
    email, password = get_email_credentials('credentials.txt')


    # Email parameters
    sender_email = email
    receiver_email = get_receiver_email('receiver_email.txt')
    subject = f"Reports for {str(datetime.date.today())}"
    body = report_scraper.generate_reports()

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    # Connect to the Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to your Gmail account
    server.login(email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Close the server connection
    server.quit()

if __name__ == '__main__':
    main()
