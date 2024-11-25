from django.urls import path
from .views import *
urlpatterns = [

    #path('app/auth', auth),
    #path('app/list_chats', list_chats),
    #path('app/create_chat', create_chat)
    path('get_chats', get_chats),
    path('auth', auth),
    path('create_chat', create_chat),
    path('get_id_user', get_id_user),

]