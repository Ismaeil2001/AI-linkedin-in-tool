import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

SID = os.getenv("TWILIO_SID")
AUTH = os.getenv("TWILIO_AUTH")
FROM_NUM = os.getenv("TWILIO_WHATSAPP_FROM")  # e.g. whatsapp:+14155238886
TO_NUM = os.getenv("TWILIO_WHATSAPP_TO")      # e.g. whatsapp:+971501279082

client = Client(SID, AUTH)

def send_whatsapp_via_twilio(message):
    msg = client.messages.create(
        body=message,
        from_=FROM_NUM,
        to=TO_NUM
    )
    print(f"Twilio sent message SID: {msg.sid}")
