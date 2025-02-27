import imaplib
import email
from email.header import decode_header
from twilio.rest import Client
import time
import schedule

# Twilio configuration
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
twilio_whatsapp_number = 'whatsapp:+14155238886'
recipient_phone_number = 'whatsapp:+91xxxxxxxxxx'

# Email configuration
EMAIL = 'vivekandteam848@gmail.com'  # Your email address
PASSWORD = 'rhtu blum maop cyom'   # Your email password or app password
IMAP_SERVER = 'imap.gmail.com'   # Change if using a different provider

def check_email():
    # Connect to the email server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)

    # Select the mailbox you want to check
    mail.select('inbox')

    # Search for all emails
    status, messages = mail.search(None, 'UNSEEN')  # Change 'UNSEEN' to 'ALL' to check all emails
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        res, msg = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])

        # Decode email subject
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        # Get the sender email
        sender = msg['From']

        # Get the email body
        if msg.is_multipart():
            body = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        # Prepare the message to send via WhatsApp
        message_body = f"From: {sender}\nSubject: {subject}\n\n{body}"
        send_whatsapp_message(message_body)

    mail.logout()

def send_whatsapp_message(body):
    message = client.messages.create(
        body=body,
        from_=twilio_whatsapp_number,
        to=recipient_phone_number
    )
    print(f'Message sent: {message.sid}')

# Schedule the email check every minute
# Schedule the email check every minute
schedule.every(1).minutes.do(check_email)

print("Checking for new emails...")
while True:
    schedule.run_pending()
    time.sleep(1)  # Correctly added argument
