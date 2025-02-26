import imaplib
import email
from email.header import decode_header
import twilio
from twilio.rest import Client
import time
import schedule

# Twilio configuration
account_sid = 'AC7aff6c2f221e608eceed18a943ff34c1'  # Replace with your Twilio Account SID
auth_token = '760e245b34f89d66dcc4d77cdff3e2c5'      # Replace with your Twilio Auth Token
client = Client(account_sid, auth_token)
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Replace with your Twilio WhatsApp number

# List of recipient phone numbers
recipient_phone_numbers = [
    'whatsapp:+91xxxxxxxxxx',  # Replace with the first recipient's WhatsApp number
    'whatsapp:+91xxxxxxxxxx',  # Add more numbers as needed
    'whatsapp:+91xxxxxxxxxx'   # Another example
]

# Email configuration
EMAIL = 'vivekandteam848@gmail.com'  # Replace with your email address
PASSWORD = 'mavg ksqr cmiu kncl'   # Replace with your app password (not your regular password)
IMAP_SERVER = 'imap.gmail.com'   # Change if using a different provider

# Specify the sender's email address to filter
specific_sender = 'saipranaygoud18@gmail.com'  # Replace with the sender's email address you want to filter

def check_email():
    try:
        # Connect to the email server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        # Select the mailbox you want to check
        mail.select('inbox')

        # Search for unseen emails from a specific sender
        status, messages = mail.search(None, f'(UNSEEN FROM "{specific_sender}")')
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
        for recipient in recipient_phone_numbers:
            message = client.messages.create(
                body=body,
                from_=twilio_whatsapp_number,
                to=recipient
            )
            print(f'Message sent to {recipient}: {message.sid}')
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