from django.contrib.auth.models import User
from django.db import models

from humans import enums


class Client(models.Model):
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    sim_sid = models.CharField(max_length=64)
    default_sms_behavior = models.PositiveSmallIntegerField(choices=enums.enum_to_choices(enums.OutgoingBehavior))
    default_voice_behavior = models.PositiveSmallIntegerField(choices=enums.enum_to_choices(enums.OutgoingBehavior))


class Caregiver(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    phone_number = models.CharField(max_length=16)


class CareRelationship(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.DO_NOTHING)


class OutsidePerson(models.Model):
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)

    # warning: sometimes, not all permissions are necessary, so proceed with caution
    awaiting_recipient_permission = models.BooleanField(default=False)  # awaiting permission from recipient
    awaiting_caregiver_permission = models.BooleanField(default=False)  # awaiting permission from caregiver
    has_recipient_permission = models.BooleanField(default=False)  # has recipient permission
    has_caregiver_permission = models.BooleanField(default=False)  # has caregiver permission
    has_explicit_permission = models.BooleanField(default=False)

    def can_sms(self):
        if self.client.default_sms_behavior == enums.OutgoingBehavior.ALLOW:
            return True

        if self.client.default_sms_behavior == enums.OutgoingBehavior.BLOCK:
            return False
