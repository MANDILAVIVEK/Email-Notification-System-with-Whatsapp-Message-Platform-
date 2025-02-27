import imaplib
import email
from email.header import decode_header
from twilio.rest import Client
import time
import schedule

# Twilio configuration
account_sid = ''  # Replace with your Twilio Account SID
auth_token = ''      # Replace with your Twilio Auth Token
client = Client(account_sid, auth_token)
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Replace with your Twilio WhatsApp number
recipient_phone_number = 'whatsapp:+91xxxxxxxxx'  # Replace with the recipient's WhatsApp number

# Email configuration
EMAIL = 'vivekandteam848@gmail.com'  # Replace with your email address
PASSWORD = 'mavg ksqr cmiu kncl'   # Replace with your app password (not your regular password)
IMAP_SERVER = 'imap.gmail.com'   # Change if using a different provider

def check_email():
    try:
        # Connect to the email server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        # Select the mailbox you want to check
        mail.select('inbox')

        # Search for all unseen emails
        status, messages = mail.search(None, 'UNSEEN')  # Change 'ALL' back to 'UNSEEN' to check only unseen emails
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

    except Exception as e:
        print(f"An error occurred: {e}")

def send_whatsapp_message(body):
    try:
        message = client.messages.create(
            body=body,
            from_=twilio_whatsapp_number,
            to=recipient_phone_number
        )
        print(f'Message sent: {message.sid}')
    except Exception as e:
        print(f"Failed to send message: {e}")

# Schedule the email check every minute
schedule.every(1).minutes.do(check_email)

print("Checking for new emails...")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second
except KeyboardInterrupt:
    print("Email checking stopped by user.")
