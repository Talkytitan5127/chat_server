from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import User, Chat, Message

def read_data(request):
    body = request.read().decode()
    data = json.loads(body)
    return data

def user_add(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    data = read_data(request)
    username = data['username']

    user, created = User.objects.get_or_create(username=username)
    if not created:
        return HttpResponseServerError('user already exists')

    return JsonResponse({
        'id':user.id
        })

def create_chat(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    data = read_data(request)
    
    chatname = data['name']
    users = data['users']

    chat, created = Chat.objects.get_or_create(name=chatname)
    if not created:
        return HttpResponseServerError('chat already exists')

    for user_id in users:
        try:
            user = User.objects.get(id=user_id)
            chat.users.add(user)
        except ObjectDoesNotExist:
          chat.delete()
          return HttpResponseNotFound('user doesn\'t exists')

    return JsonResponse({
        'id':chat.id,
        })

def send_message(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    data = read_data(request)

    chat = get_object_or_404(Chat, id=data['chat'])
    user = get_object_or_404(User, id=data['author'])
    
    message = Message.objects.create(chat=chat, author=user, text=data['text'])
    
    return JsonResponse({
        'id':message.id,
        })

def get_list_chats(request):
    pass


def get_list_messages(request):
    pass
