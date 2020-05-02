from django.urls import path

from telephony.views import incoming, outgoing

urlpatterns = [
    path('incoming-sms/', incoming.incoming_sms),
    path('incoming-voice/', incoming.incoming_voice),
    path('outgoing-sms/', outgoing.outgoing_sms),
]
