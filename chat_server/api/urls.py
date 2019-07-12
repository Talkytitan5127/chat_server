from django.urls import path
from api import views

urlpatterns = [
    path('users/add', views.user_add, name='user_add'),
    path('chats/add', views.create_chat, name='create_chat'),
    path('chats/get', views.get_list_chats, name='get_chats_of_user'),
    path('messages/add', views.send_message, name='send_message'),
    path('messages/get', views.get_list_messages, name='list_mes_in_chat'),
]