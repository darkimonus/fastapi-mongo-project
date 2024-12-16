from twilio.rest import Client
from conf import config
from custom_logging.middleware import logger

account_sid = config.get('TWILIO_SID')
auth_token = config.get('TWILIO_SECRET')
client = Client(account_sid, auth_token)


def send_code(phone_number: str, code: str):
    message = client.messages.create(
        body=f'Your verification code is {code}',
        from_='+1234567890',
        to=phone_number
    )
    return message
