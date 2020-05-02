from django_twilio.decorators import twilio_view
from twilio.twiml import TwiML
from twilio.twiml.messaging_response import MessagingResponse

from humans.models import Client


@twilio_view
def incoming_sms(request) -> TwiML:
    print(request.POST)
    to_ = request.POST.get('To')
    client = Client.objects.get(phone_number=to_)

    resp = MessagingResponse()
    resp.message(body=request.POST.get('Body'),
                 to=client.sim_sid,
                 from_=request.POST.get('From'))
    return resp


@twilio_view
def incoming_voice(request):
    pass
