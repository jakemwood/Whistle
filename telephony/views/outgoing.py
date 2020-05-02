from django.http import HttpResponse
from django_twilio.decorators import twilio_view
from twilio.twiml import TwiML
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

from humans.enums import OutgoingBehavior
from humans.models import OutsidePerson, Client
from telephony.utils import get_twilio_client


def send_sms(sim_sid, destination, body) -> TwiML:
    client = Client.objects.get(sim_sid=sim_sid)

    resp = MessagingResponse()
    resp.message(body=body,
                 to=destination,
                 from_=client.phone_number)
    return resp


@twilio_view
def outgoing_sms(request) -> TwiML:
    print(request.POST)

    destination = request.POST.get('To')
    sim_sid = request.POST.get('From')

    # First, find if this person is already a known recipient with rules.
    try:
        op = OutsidePerson.objects.get(phone_number=destination,
                                       client__sim_sid=sim_sid)
        if op.allowed_to_communicate:
            return send_sms(sim_sid, destination, request.POST.get('Body'))

    except OutsidePerson.DoesNotExist:

        # Deal with the defaults of the client
        try:
            client = Client.objects.get(sim_id=request.POST.get('From'))

            if client.default_sms_behavior == OutgoingBehavior.BLOCK:
                return MessagingResponse()

            if client.default_sms_behavior == OutgoingBehavior.ALLOW:
                return send_sms(sim_sid, destination, request.POST.get('Body'))

            if client.default_sms_behavior == OutgoingBehavior.SEEK_PERMISSION_CAREGIVER or \
                    client.default_sms_behavior == OutgoingBehavior.SEEK_ALL_PERMISSION:
                pass

            if client.default_sms_behavior == OutgoingBehavior.SEEK_PERMISSION_RECIPIENT or \
                    client.default_sms_behavior == OutgoingBehavior.SEEK_ALL_PERMISSION:
                pass

        except Client.DoesNotExist:
            return MessagingResponse()

    return MessagingResponse()


@twilio_view
def outgoing_voice(request):
    return VoiceResponse().reject()
