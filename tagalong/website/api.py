from website.models import Event, EventTemplate
from .serializers import EventSerializer, EventTemplateSerializer
from datetime import datetime
from rest_framework.response import Response
from accounts.models import User
from rest_framework.views import APIView
import logging
from accounts.serializers import UserSerializer
from rest_framework import status
logger = logging.getLogger('django')


class TemplateEventsList(APIView):

    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        templete_events = EventTemplate.objects.filter(
            user=user).order_by('title')
        templates_serializer = EventTemplateSerializer(
            templete_events, many=True)
        users_ids = [template['user']
                     for template in templates_serializer.data]
        users_serializer = UserSerializer(
            User.objects.filter(id__in=users_ids), many=True)
        for i, template in enumerate(templates_serializer.data):
            user = list(
                filter(lambda x: x['id'] == template['user'], users_serializer.data))[0]
            invites_serializer = UserSerializer(User.objects.filter(
                pk__in=templates_serializer.data[i]['invites']), many=True)
            for j, invite in enumerate(invites_serializer.data):
                templates_serializer.data[i]['invites'][j] = invite
                templates_serializer.data[i]['user'] = user
        return Response(templates_serializer.data)

    # TODO here the user is in the formdata and not in the url!! how to do? request.data={user:['1']}
    def post(self, request, pk=None):
        data = request.data
        data._mutable = True
        data['date'] = datetime.strptime(data['date'], '%m/%d/%Y')
        serializer = EventTemplateSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            info_message = {
                'msg': f'Template {serializer.data["title"]} created', 'msgType': 'info'}
            return Response(data={**serializer.data, **info_message}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateById(APIView):

    def get(self, request, pk=None):
        template = EventTemplate.objects.get(pk=pk)
        template_serializer = EventSerializer(template)
        user_serializer = UserSerializer(User.objects.get(pk=template.user.id))
        return Response({**template_serializer.data, **user_serializer.data})

    def put(self, request, pk=None):
        template = EventTemplate.objects.get(pk=pk)
        data = request.data
        data._mutable = True
        data['date'] = datetime.strptime(data['date'], '%m/%d/%Y')
        serializer = EventTemplateSerializer(template, data=data)
        if serializer.is_valid():
            serializer.save()
            info_message = {
                'msg': {'info': f'Template {serializer.data["title"]} updated'}}
            return Response(data=info_message, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        template = EventTemplate.objects.get(pk=pk)
        serializer = EventTemplateSerializer(template)
        info_message = {'msgType': 'info',
                        'msg': f'Deleted template {template.title}'}
        template.delete()
        return Response({**serializer.data, **info_message})


class EventsList(APIView):

    def get(self, request):
        events_serializer = EventSerializer(
            Event.objects.all().order_by('title'), many=True)
        users_ids = [template['user'] for template in events_serializer.data]
        users_serializer = UserSerializer(
            User.objects.filter(id__in=users_ids), many=True)
        for i, template in enumerate(events_serializer.data):
            user = list(
                filter(lambda x: x['id'] == template['user'], users_serializer.data))[0]
            events_serializer.data[i]['user'] = user
            invites_serializer = UserSerializer(User.objects.filter(
                pk__in=events_serializer.data[i]['invites']), many=True)
            for j, invite in enumerate(invites_serializer.data):
                events_serializer.data[i]['invites'][j] = invite
            participants_serializer = UserSerializer(User.objects.filter(
                pk__in=events_serializer.data[i]['participants']), many=True)
            for j, participant in enumerate(participants_serializer.data):
                events_serializer.data[i]['participants'][j] = participant
        return Response(events_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        data = request.data
        data._mutable = True
        data['date'] = datetime.strptime(data['date'], '%m/%d/%Y')
        serializer = EventSerializer(data=data, many=False)
        if serializer.is_valid():
            user = User.objects.get(pk=pk)
            serializer.save(user=user)
            info_message = {
                'msg': f'Event {serializer.data["title"]} created', 'msgType': 'info'}
            return Response(data={**serializer.data, **info_message}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsById(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist as e:
            return Response({"error": "Not found."}, status=404)

    def get(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        event_serializer = EventSerializer(event)
        user_serializer = UserSerializer(User.objects.get(pk=event.user.id))
        return Response({**event_serializer.data, **user_serializer.data})

    def put(self, request, pk=None, action=None, target=None):
        event = Event.objects.get(pk=pk)
        if action == 'attend':
            event.participants.add(User.objects.get(pk=target))
            event.save()
            return Response('', status=200)
        elif action == 'decline':
            event.participants.remove(User.objects.get(pk=target))
            event.save()
            return Response('', status=200)
        else:
            data = request.data
            data._mutable = True
            data['date'] = datetime.strptime(data['date'], '%m/%d/%Y')
            serializer = EventSerializer(event, data=data)
            if serializer.is_valid():
                serializer.save()
                info_message = {
                    'msg': f'Event {serializer.data["title"]} updated', 'msgType': 'info'}
            return Response(data={**serializer.data, **info_message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        info_message = {
            'msg': f'Deleted Event {Event.title}', 'msgType': 'info'}
        event.delete()
        return Response({**serializer.data, **info_message})
