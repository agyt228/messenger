import random

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from app.models import *
import json
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers
'''from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render
from app.models import *
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def auth(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        if User.objects.filter(login=login).exists():
            user = User.objects.filter(login=login).first()
            if check_password(password, user.password):
                token = user.token
                return HttpResponse(json.dumps({'status': 'ok', 'token': token}))
            else:
                return HttpResponse(json.dumps({'status': 'error password'}))
        else:
            return HttpResponse(json.dumps({'status': 'error login'}))


@csrf_exempt
def list_chats(request):
    if request.method == 'POST':
        token = request.POST['token']
        if User.objects.filter(token=token).exists():
            user = User.objects.filter(token=token).first()
            chats = Chat.objects.filter(admin_chat=user)

            chats_dict = []
            for chat in chats:
                chats_dict.append({
                    'id': chat.id,
                    'title': chat.title,
                    'description': chat.description,
                    'avatar': f'/media/{chat.avatar}'
                })

            return HttpResponse(json.dumps({'status': 'ok', 'chat': chats_dict}))
        else:
            return HttpResponse({'status': '403'})
@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        token = request.POST['token']
        if User.objects.filter(token=token).exists():
            title = request.POST['title']
            description = request.POST['description']
            admin_chat = User.objects.filter(token=token).first()

            chat = Chat()
            chat.title = title
            chat.description = description
            chat.admin_chat = admin_chat
            chat.save()
            return HttpResponse(json.dumps({'status': 'ok'}))
        else:
            return HttpResponse({'status': '403'})'''
@csrf_exempt
def get_chats(request):
    if request.method == 'POST':
        id_user = request.POST['id_user']
        token = request.POST['token']

        if get_object_or_404(User, id=id_user).token != token:
            return HttpResponse('403')
        else:
            user = get_object_or_404(User, id=id_user)
            chats = Chat.objects.filter(admin_chat=user)
            chats_new = []
            for chat in chats:
                members = []
                for member in chat.users.all():
                    members.append({
                        'id': member.id,
                        'login': member.login,
                        'avatar': f'/media/{str(member.avatar)}'
                    })
                chats_new.append({
                    'id': chat.id,
                    'title': chat.title,
                    'description': chat.description,
                    'avatar': f'{str(chat.avatar)}',
                    'users': members
                })
            return HttpResponse(json.dumps(chats_new))
    else:
        return HttpResponse('Данные охраняются саблизубыми котиками^^')

@csrf_exempt
def get_id_user(request):
    token = request.POST['token']
    user = User.objects.filter(token=token).first()
    return HttpResponse(json.dumps({'id_user': user.id}))

@csrf_exempt
def auth(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        if User.objects.filter(login=login).exists():
            user = User.objects.filter(login=login).first()
            if check_password(password, user.password):
                token = user.token
                return HttpResponse(json.dumps({'status': 'ok', 'token': token}))
            else:
                return HttpResponse(json.dumps({'status': 'error password'}))
        else:
            return HttpResponse(json.dumps({'status': 'error login'}))


@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        id_creator = int(request.POST['id_creator'])
        title = request.POST['title']
        description = request.POST['description']
        creator = get_object_or_404(User, id=id_creator)

        chat = Chat(title=title, description=description, creator=creator)
        chat.save()
        chat.users.add(creator)
        return HttpResponse(json.dumps({'status': 'ok'}))
    else:
        return HttpResponse(json.dumps({'status': 'Error post request'}))

def generate_Token():
    s = 'asdfklewjtwogkassdkGGUYGUYGUYTFlgfnmsdklgnhythbGUYHJERIGVKGIfdfsdf564643wjklegnweklfgfgerygfyegydfgYYYGY656565rfyrgye'
    return ''.join([s[random.randint(0, len(s) - 1)] for i in range(32)])