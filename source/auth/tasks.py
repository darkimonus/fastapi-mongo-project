from twilio.rest import Client
from conf import config
from celery_conf import celery_app
from custom_logging.middleware import logger

sms_service = config.get('DEFAULT_SMS_SERVICE')
account_sid = config.get('TWILIO_SID')
auth_token = config.get('TWILIO_SECRET')
sender_phone = config.get('TWILIO_SENDER_PHONE')
client = Client(account_sid, auth_token)


@celery_app.task(bind=True)
def send_sms_code(phone_number: str, code: str, service_name: str = sms_service):
    if service_name == 'TWILIO':
        message = client.messages.create(
            body=f'Your verification code is {code}',
            from_='+1234567890',
            to=phone_number
        )
        return message
    else:
        raise ValueError(f"Sms service named {sms_service} doesn't exist or is not supported.")
