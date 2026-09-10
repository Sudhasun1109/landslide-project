import os
from twilio.rest import Client


def send_sms(message_body, receiver_number):

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not account_sid:
        raise Exception("TWILIO_ACCOUNT_SID is missing")

    if not auth_token:
        raise Exception("TWILIO_AUTH_TOKEN is missing")

    if not twilio_number:
        raise Exception("TWILIO_PHONE_NUMBER is missing")

    client = Client(
        account_sid,
        auth_token
    )

    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=receiver_number
    )

    return message.sid