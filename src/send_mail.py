import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import sender_address, sender_password, sender_server, sender_port

class Message:
    html = ''
    text = ''

    def __init__(self, name):
        self.html = open(f'email/{name}.html', 'r').read()
        self.text = open(f'email/{name}.txt', 'r').read()

    def format(self, key, value):
        self.html = self.html.replace(key, value)
        self.text = self.text.replace(key, value)
        return self

FORGOT_PASSWORD = Message('forgot_password')
NEW_USER        = Message('new_user')

def sendEmail(receiver_email: str, subject: str, message: Message):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_address
    msg['To'] = receiver_email

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(message.text, "plain")
    part2 = MIMEText(message.html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP_SSL(sender_server, sender_port)
    try:
        server.login(sender_address, sender_password)
    except:
        print('[!] Failed to login to mail server')

    try:
        server.sendmail(sender_address, receiver_email, msg.as_string())
    except:
        print('[!] Failed to send email')

    server.quit()

def sendNewUserEmail(receiver_email: str, user_password: str):
    sendEmail(receiver_email, 'Welcome to Rewards Points!', NEW_USER.format('{user_password}', user_password))

def sendForgotPasswordEmail(receiver_email: str, user_password: str):
    sendEmail(receiver_email, 'Your Rewards Points Password', FORGOT_PASSWORD.format('{user_password}', user_password))