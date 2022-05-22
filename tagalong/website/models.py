from accounts.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
import json
import logging
logger = logging.getLogger("mylogger")


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(null=True, blank=True, max_length=600)
    date = models.DateTimeField(null=True, blank=True)
    # link = models.URLField(max_length = 200,null=True,blank=True)
    # link_text = models.CharField(max_length=40,null=True,blank=True)
    adress_link = models.URLField(max_length=200, null=True, blank=True)
    adress = models.CharField(max_length=50, null=True, blank=True)
    invites = models.ManyToManyField(
        User, blank=True, related_name='invites_event_set')
    participants = models.ManyToManyField(
        User, blank=True, related_name='participants_event_set')

    def __str__(self):
        return f'{self.user.username} {self.title}'


class EventTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(null=True, blank=True, max_length=600)
    date = models.DateTimeField(null=True, blank=True)
    adress_link = models.URLField(max_length=200, null=True, blank=True)
    adress = models.CharField(max_length=50, null=True, blank=True)
    invites = models.ManyToManyField(
        User, blank=True, related_name='invites_template_set')
