import os
from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    try:
        # Replace these with your Twilio credentials
        TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to
        )
        return {'success': True, 'sid': message.sid}
    except Exception as e:
        return {'success': False, 'error': str(e)}
