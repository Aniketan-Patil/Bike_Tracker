# serviceapp/sms_notifications.py
import os
from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    # Initialize Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send SMS
    message_response = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )

    # Log the message SID and status
    print(f"Message SID: {message_response.sid}")
    print(f"Message Status: {message_response.status}")
