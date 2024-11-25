from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('logout', logout),
    path('app/panel', panel),
    path('create_chat', create_chat),
    path('delete/<int:id>', delete_chat),
    path('chat/<int:id>', chat),
    path('ajax', ajax),
    path('delete/<int:id>/<int:id_chat>', delete_message),
    path('ajax_add_audio', ajax_add_audio),
    path('update_chat', update_chat)
]
