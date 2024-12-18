from twilio.rest import Client
from conf import settings
from celery_conf import celery_app
from custom_logging.middleware import logger

client = Client(
    account_sid=settings.twilio.twilio_sid,
    password=settings.twilio.twilio_auth_token
)


@celery_app.task(bind=True)
def send_sms_code(phone_number: str, code: str, service_name: str = 'TWILIO'):
    if service_name == 'TWILIO':
        message = client.messages.create(
            body=f'Your verification code is {code}',
            from_='+1234567890',
            to=phone_number
        )
        return message
    else:
        raise ValueError(f"Sms service named {service_name} doesn't exist or is not supported.")
