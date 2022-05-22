from rest_framework import serializers
from website.models import Event,EventTemplate
from accounts.models import User 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('__all__')

class EventTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTemplate
        fields = ('__all__')