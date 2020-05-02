from django.db import models

# Create your models here.
from humans.models import Client


class MessageQueue(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    to = models.CharField(max_length=16)
    body = models.CharField(max_length=160)
    date_created = models.DateTimeField(auto_created=True)
