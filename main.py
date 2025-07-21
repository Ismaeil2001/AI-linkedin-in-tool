from linkedin_scraper import scrape_latest_post
from twilio.rest import Client
import os

# Get environment variables
twilio_sid = os.environ.get("TWILIO_SID")
twilio_auth = os.environ.get("TWILIO_AUTH")
twilio_from = os.environ.get("TWILIO_WHATSAPP_FROM")
twilio_to = os.environ.get("TWILIO_WHATSAPP_TO")

# Create Twilio client
client = Client(twilio_sid, twilio_auth)

# PROFILE_URL can be changed back later after testing
profile_url = "https://www.linkedin.com/in/INSERT-ACTUAL-PROFILE-HERE"

# TEMPORARY OVERRIDE: Replace scrape with a test message
post = "✅ This is a test message from the GitHub Action LinkedIn Bot."

# Print values to debug in GitHub Actions log
print("Twilio From:", twilio_from)
print("Twilio To:", twilio_to)
print("Message Body:", post)

# Send the WhatsApp message
try:
    message = client.messages.create(
        body=post,
        from_=twilio_from,
        to=twilio_to
    )
    print("Twilio SID:", message.sid)
    print("Message Status:", message.status)
except Exception as e:
    print("Error sending WhatsApp message:", str(e))

