from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    GroupSerializer,
    HashtagSerializer,
    MessageSerializer,
    MessageUpdateSerializer,
    MessageReactionsSerializer,
    ThreadMessageSerializer,
    ThreadMessageUpdateSerializer,
    ThreadMessageReactionsSerializer,
)
from .utils import (
    STATUS_CODE_200_DELETE,
    STATUS_CODE_400,
    STATUS_CODE_403,
    STATUS_CODE_404,
    STATUS_CODE_405,
)
from rest_framework import viewsets
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message, User, Group, Hashtag, ThreadMessage
import datetime
import json


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows hashtags to be viewed or edited.
    """
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = GroupSerializer


class ThreadMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows threads to be viewed or edited.
    """
    queryset = ThreadMessage.objects.all()
    serializer_class = UserSerializer


# User Views
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def get_user(request):
    if request.method == 'GET':
        data = request.GET
        user_id = data.get('user_id', None)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                serializer = UserSerializer(user[0])
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                serializer = UserUpdateSerializer(user[0], data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        serializer.data, safe=False, status=200)
                return JsonResponse(serializer.errors, status=400)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        if user_id:
            user = User.objects.filter(id=user_id)
            if user:
                user[0].delete()
                return JsonResponse(
                    STATUS_CODE_200_DELETE, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    else:
        return JsonResponse(STATUS_CODE_405, status=405)


# Group Views
@csrf_exempt
def get_group(request):
    if request.method == 'GET':
        data = request.GET
        group_id = data.get('group_id', None)
        if group_id:
            group = Group.objects.filter(id=group_id)
            if group:
                serializer = GroupSerializer(group[0])
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        group_id = data.get('group_id', None)
        if group_id:
            group = Group.objects.filter(id=group_id)
            if group:
                serializer = GroupSerializer(group[0], data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        serializer.data, safe=False, status=200)
                return JsonResponse(serializer.errors, status=400)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        group_id = data.get('group_id', None)
        if group_id:
            group = Group.objects.filter(id=group_id)
            if group:
                group[0].delete()
                return JsonResponse(
                    STATUS_CODE_200_DELETE, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    else:
        return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def new_group(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def group_member(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        group_id = data.get('group_id', None)
        if user_id and group_id:
            user = User.objects.filter(id=user_id)
            group = Group.objects.filter(id=group_id)
            if user and group:
                group[0].members.add(user[0])
                serializer = GroupSerializer(group[0])
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        group_id = data.get('group_id', None)
        if user_id and group_id:
            user = User.objects.filter(id=user_id)
            group = Group.objects.filter(id=group_id)
            if user and group:
                group[0].members.remove(user[0])
                serializer = GroupSerializer(group[0])
                return JsonResponse(
                    serializer.data, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    else:
        return JsonResponse(STATUS_CODE_405, status=405)


# Message Views
@csrf_exempt
def get_message(request):
    if request.method == 'GET':
        data = request.GET
        message_id = data.get('message_id', None)
        if message_id:
            message = Message.objects.filter(id=message_id)
            if message:
                serializer = MessageSerializer(message[0])
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        message_id = data.get('message_id', None)
        if message_id:
            message = Message.objects.filter(id=message_id)
            if message:
                serializer = MessageUpdateSerializer(message[0], data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        serializer.data, safe=False, status=200)
                return JsonResponse(serializer.errors, status=400)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        message_id = data.get('message_id', None)
        if message_id:
            message = Message.objects.filter(id=message_id)
            if message:
                message[0].delete()
                return JsonResponse(
                    STATUS_CODE_200_DELETE, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    else:
        return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def post_message(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        group_id = data.get('group_id', None)
        text = data.get('text', None)
        if user_id and group_id and text:
            user = User.objects.filter(id=user_id)
            group = Group.objects.filter(id=group_id)
            if user and group:
                message = Message(
                    author=user[0],
                    group=group[0],
                    text=text,
                ).publish()
                serializer = MessageSerializer(message)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def like_message(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        message_id = data.get('message_id', None)
        if user_id and message_id:
            user = User.objects.filter(id=user_id)
            message = Message.objects.filter(id=message_id)
            if user and message:
                if user[0] in message[0].dislikers.all():
                    return JsonResponse(STATUS_CODE_403, status=403)
                if user[0] not in message[0].likers.all():
                    message[0].likers.add(user[0])
                    serializer = MessageSerializer(message[0])
                    return JsonResponse(serializer.data, status=201)
                else:
                    message[0].likers.remove(user[0])
                    serializer = MessageSerializer(message[0])
                    return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def dislike_message(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        message_id = data.get('message_id', None)
        if user_id and message_id:
            user = User.objects.filter(id=user_id)
            message = Message.objects.filter(id=message_id)
            if user and message:
                if user[0] in message[0].likers.all():
                    return JsonResponse(STATUS_CODE_403, status=403)
                if user[0] not in message[0].dislikers.all():
                    message[0].dislikers.add(user[0])
                    serializer = MessageSerializer(message[0])
                    return JsonResponse(serializer.data, status=201)
                else:
                    message[0].dislikers.remove(user[0])
                    serializer = MessageSerializer(message[0])
                    return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def get_message_reactions(request):
    if request.method == 'GET':
        data = request.GET
        message_id = data.get('message_id', None)
        limit = data.get('limit', 50)
        if message_id:
            message = Message.objects.filter(id=message_id)
            if message:
                serializer = MessageReactionsSerializer(message[0])
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def post_comment(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        message_id = data.get('message_id', None)
        text = data.get('text', None)
        if user_id and message_id and text:
            user = User.objects.filter(id=user_id)
            message = Message.objects.filter(id=message_id)
            if user and message:
                thread = ThreadMessage(
                    author=user[0],
                    message=message[0],
                    text=text,
                ).publish()
                serializer = ThreadMessageSerializer(thread)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        thread_id = data.get('thread_id', None)
        if thread_id:
            thread = ThreadMessage.objects.filter(id=thread_id)
            if thread:
                serializer = ThreadMessageUpdateSerializer(thread[0], data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        serializer.data, safe=False, status=200)
                return JsonResponse(serializer.errors, status=400)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        thread_id = data.get('thread_id', None)
        if thread_id:
            thread = ThreadMessage.objects.filter(id=thread_id)
            if thread:
                thread[0].delete()
                return JsonResponse(
                    STATUS_CODE_200_DELETE, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)

    else:
        return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def like_thread(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        thread_id = data.get('thread_id', None)
        if user_id and thread_id:
            user = User.objects.filter(id=user_id)
            thread = ThreadMessage.objects.filter(id=thread_id)
            if user and thread:
                if user[0] in thread[0].dislikers.all():
                    return JsonResponse(STATUS_CODE_403, status=403)
                if user[0] not in thread[0].likers.all():
                    thread[0].likers.add(user[0])
                    serializer = ThreadMessageSerializer(thread[0])
                    return JsonResponse(serializer.data, status=201)
                else:
                    thread[0].likers.remove(user[0])
                    serializer = ThreadMessageSerializer(thread[0])
                    return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def dislike_thread(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_id = data.get('user_id', None)
        thread_id = data.get('thread_id', None)
        if user_id and thread_id:
            user = User.objects.filter(id=user_id)
            thread = ThreadMessage.objects.filter(id=thread_id)
            if user and thread:
                if user[0] in thread[0].likers.all():
                    return JsonResponse(STATUS_CODE_403, status=403)
                if user[0] not in thread[0].dislikers.all():
                    thread[0].dislikers.add(user[0])
                    serializer = ThreadMessageSerializer(thread[0])
                    return JsonResponse(serializer.data, status=201)
                else:
                    thread[0].dislikers.remove(user[0])
                    serializer = ThreadMessageSerializer(thread[0])
                    return JsonResponse(serializer.data, status=201)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def get_thread_reactions(request):
    if request.method == 'GET':
        data = request.GET
        thread_id = data.get('thread_id', None)
        limit = data.get('limit', 50)
        if thread_id:
            thread = ThreadMessage.objects.filter(id=thread_id)
            if thread:
                serializer = ThreadMessageReactionsSerializer(thread[0])
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse(
                STATUS_CODE_404, status=404)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def search_hashtag(request):
    if request.method == 'GET':
        data = request.GET
        hashtag_text = data.get('text', None)
        limit = data.get('limit', 50)
        if hashtag_text:
            hashtag = Hashtag.objects.filter(text=hashtag_text)
            messages = Message.objects.filter(hashtags__text=hashtag_text)
            if messages:
                serializer = MessageSerializer(messages, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse([], safe=False, status=200)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)


@csrf_exempt
def search_username(request):
    if request.method == 'GET':
        data = request.GET
        username = data.get('username', None)
        limit = data.get('limit', 50)
        if username:
            user = User.objects.filter(username=username)
            if user:
                messages = user[0].messages.all()
                serializer = MessageSerializer(messages, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            return JsonResponse([], safe=False, status=200)
        return JsonResponse(
            STATUS_CODE_400, status=400)
    return JsonResponse(STATUS_CODE_405, status=405)
