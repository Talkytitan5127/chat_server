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
    print(request)
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
    user = get_object_or_404(chat.users, id=data['author'])
    
    message = Message.objects.create(chat=chat, author=user, text=data['text'])
    
    return JsonResponse({
        'id':message.id,
        })

def get_list_chats(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    data = read_data(request)

    user = get_object_or_404(User, id=data['user'])
    chats = user.chat_set.all()

    list_chats = []
    for chat in sorted(chats,
        key=lambda chat:chat.message_set.order_by('created_at').last().created_at, reverse=True):
        packet = {
            'chat_id': chat.id,
            'name': chat.name,
            'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'users_id': list(map(lambda user: user.id, chat.users.all())),
        }
        list_chats.append(packet)

    return JsonResponse({'chats':list_chats})


def get_list_messages(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    data = read_data(request)

    messages = Message.objects.filter(chat=data['chat']).order_by('created_at')
    
    list_messages = []
    for message in messages:
        packet = {
            'chat_id': message.chat.id,
            'author_id': message.author.id,
            'text': message.text,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        list_messages.append(packet)
    
    return JsonResponse({'messages':list_messages})
