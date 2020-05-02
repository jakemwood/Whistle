import os

from twilio.rest import Client


def get_twilio_client():
    return Client(os.environ.get('TWILIO_ACCOUNT_SID'),
                  os.environ.get('TWILIO_AUTH_TOKEN'))
