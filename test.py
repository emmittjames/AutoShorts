import smtplib, configparser

def send_email(sender_email, sender_password, recipient_email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        email_content = f'Subject: {subject}\n\n{message}'
        server.sendmail(sender_email, recipient_email, email_content)

config = configparser.ConfigParser()
config.read('config.ini')
sender_email = config["Email"]["SenderEmail"]
sender_password = config["Email"]["SenderPassword"]
recipient_email = config["Email"]["RecipientEmail"]
subject = 'Test Email'
message = 'This is a test email sent from Python using Gmail SMTP.'

send_email(sender_email, sender_password, recipient_email, subject, message)