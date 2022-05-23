from accounts.models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializers
from tagalong.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
import ast
import json
from django.core import serializers
from rest_framework.response import Response
from website.models import Event
from rest_framework.views import APIView
import logging
from rest_framework import status
logger = logging.getLogger('django')


class UserById(APIView):

    def get(self, request, pk=None):
        if not pk == 'undefined' and pk:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            friends_serializer = UserSerializer(User.objects.filter(
                pk__in=serializer.data['friends']), many=True)
            serializer.data['friends'] = friends_serializer.data
            for i, friend in enumerate(friends_serializer.data):
                serializer.data['friends'][i] = friend
            return Response(serializer.data)
        return Response()

    def put(self, request, pk=None):
        data = ast.literal_eval(json.dumps(request.data))
        data['friends'] = list(map(int, data['friends'].split(',')))
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            old_friends_list = set(
                user.friends.all().values_list('pk', flat=True))
            new_friends_list = set(data['friends'])
            diff_friends = list(
                new_friends_list.symmetric_difference(old_friends_list))
            if diff_friends:
                has_added_friend = len(
                    old_friends_list) < len(new_friends_list)
                if has_added_friend:
                    FriendRequest.objects.get(
                        from_user=diff_friends[0], to_user=user.id).delete()
                    new_friend_user = User.objects.filter(
                        pk=diff_friends[0]).first()
                    if new_friend_user:
                        new_friend_user.friends.add(user)
                        new_friend_user.save()
                else:
                    friend_to_remove = User.objects.filter(
                        pk=diff_friends[0]).first()
                    if friend_to_remove:
                        friend_to_remove.friends.add(user)
                        friend_to_remove.save()
            serializer.save()
            info_message = {'msg': 'updated', 'msgType': 'info'}
            return Response(data=info_message, status=200)
        return Response(serializer.errors, status=400)

    # def delete(self, request, pk=None):
    #     user = User.objects.get(pk=pk)
    #     serializer = UserSerializer(user)
    #     info_message = {'msg': {'info': f'Deleted template {user.username}'}}
    #     user.delete()
    #     return Response({**serializer.data, **info_message})


class GetEventUsers(APIView):
    def get(self, request, pks=None):
        instances = User.objects.filter(id__in=map(int, pks.split(',')))
        serializer = UserSerializer(instances, many=True)
        return Response(serializer.data)


class GetAllUser(APIView):
    def get(self, request, pk=None):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)


class HandleFriendRequest(APIView):

    def post(self, request):
        serializer = FriendRequestSerializers(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            info_message = {'msg': 'Friend request sent', 'msgType': 'info'}
            return Response(data=info_message, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestById(APIView):

    def get(self, request, pk=None, to_or_from=True):
        if to_or_from == 'from_user':
            friend_requests = FriendRequest.objects.filter(from_user=pk)
        elif to_or_from == 'to_user':
            friend_requests = FriendRequest.objects.filter(to_user=pk)
        serializer = FriendRequestSerializers(friend_requests, many=True)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk)
        serializer = FriendRequestSerializers(friend_request)
        friend_request.delete()
        return Response(serializer.data)


class SendEmailToUsers(APIView):
    def post(self, request, pks=None, action=None, target=None):
        users = User.objects.filter(id__in=map(int, pks.split(',')))
        for user in users:
            if action == 'eventCreated':
                event = Event.objects.filter(pk=target)
                # send_mail('New TagAlong Event', 'message', EMAIL_HOST_USER, [user.email])

        # serializer = UserSerializer(instances,many=True)
        # info_message={'msg':{'info':f'Friend request sent'}}
        return Response()
