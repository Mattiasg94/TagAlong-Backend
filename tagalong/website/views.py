from multiprocessing import context
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render
from django.contrib import messages
import logging
import math
import time
import json
from tagalong.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from website.forms import NewEventForm
from website.models import Event
from django.contrib.auth.decorators import login_required
from accounts.models import User
logger = logging.getLogger("mylogger")


def events(request):
    context={}
    context['friends']=request.user.friends
    events=Event.objects.all().order_by('date')
    context['events']=events
    return render(request, 'website/events.html', context)

@login_required
def new_event(request):
    context={}
    new_event_form=NewEventForm()
    if request.method == 'POST':
        action=request.POST.get('action')
        if action=='use_template':
            event=Event.objects.get(pk=request.POST['event_id'])
            new_event_form=NewEventForm(instance=event)
        if 'post' in action:
            form = NewEventForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user=request.user
                form.save()
                messages.add_message(request,messages.INFO,f'Event {form.title} has been created.')
    context['new_event_form']=new_event_form
    context['my_templates']=Event.objects.filter(user=request.user)
    return render(request,'website/new-event.html',context)