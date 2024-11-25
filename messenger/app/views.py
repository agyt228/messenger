import base64

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import json
from .models import *
import random

def generate_token():
    s = 'aslkfhqnjlkwfjasklfjasklfjelwifhskdjgakjdasfklalfasfqwqwr'
    token = ''
    for i in range(50):
        token += s[random.randint(0, len(s) - 1)]
    return token

def index(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        password = data['password']
        if 'reg' in data:
            #обработка формы регистрации
            user = User()
            user.login = email
            user.password = make_password(password)
            user.token = generate_token()
            user.save()
        else:
            #обработка формы авторизации
            error = ''
            if User.objects.filter(login=email).exists():
                hash_password = User.objects.filter(login=email).first().password
                if check_password(password, hash_password):
                    #успешная авторизация
                    request.session['user'] = email
                    return redirect('/app/panel')
                else:
                    error += 'Password error!'
            else:
                error += 'Login error!'


    return render(request, 'index/index.html')


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('/')


def panel(request):
    if 'user' in request.session:
        chats = select_chat_user(request)
        if request.method == 'POST':
            id_user = request.POST['id_user']
            email = request.POST['email']
            password = request.POST['password']
            user = User(id=id_user)
            user.login = email
            user.password = make_password(password)
            user.save()

        current_user = User.objects.filter(login=request.session['user']).first()
        return render(request, 'panel/index.html', {'current_user': current_user, 'chats': chats})
    else:
        return redirect('/')

def create_chat(request):
    if 'user' in request.session and request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        path = 'default.png'
        if 'avatar' in request.FILES:
            img = request.FILES['avatar']
            f = FileSystemStorage()
            try:
                f.save('avatars_chat/' + img.name,img)
            except:
                pass
            path = 'avatars_chat/'+img.name

        current_user = User.objects.filter(login=request.session['user']).first()
        chat = Chat()
        chat.title = title
        chat.description = description
        chat.avatar = path
        chat.admin_chat = current_user
        chat.save()
        return redirect('app/panel')


def select_chat_user(request):
    return Chat.objects.filter(admin_chat=User.objects.filter(login=request.session['user']).first())

def delete_chat(request, id):
    if 'user' in request.session:
        Chat.objects.filter(id=id).delete()
        return redirect('/app/panel')

def chat(request, id):
    chat = Chat.objects.filter(id=id).first()
    chats = select_chat_user(request)
    messages = Message.objects.filter(chat=chat)
    users = User.objects.all()

    user_ids = []
    for user in chat.users.all():
        user_ids.append(user.id)

    return render(request, 'chat.html', {'chat': chat, 'chats': chats, 'messages': messages, 'users': users, 'user_ids': user_ids})

@csrf_exempt
def ajax(request):
    if request.method == 'POST':
        path = ''
        if request.FILES.get('file'):
            img = request.FILES['file']
            f = FileSystemStorage()
            try:
                f.save('chats/' + img.name, img)
            except:
                pass
            path = 'chats/' + img.name
        message = request.POST['message']
        chat_id = request.POST['chatId']
        user = request.session['user']
        chat = Chat.objects.filter(id=chat_id).first()
        user = User.objects.filter(login=user).first()
        m = Message()
        m.chat = chat
        m.user = user
        m.text = message
        m.file = path
        m.save()

        res = '''<div class ="message bg-secondary-subtle" ><span class ="user" >'''+user.login+'''</span><span class ="text" >'''+message+'''<i>  </i></span>'''
        if path != '':
            #if path.endswith('wav'):
            #    res += '<audio id="audioOlayback" controls style="display: block" src="/media/'+str()+'"></audio>'
            res += '<p><img src="/media/'+path+'" width="150px"></p>'

        if user.login == request.session['user']:

            res += '''<span style="color: red">
            
                    <a style="color: red" href="/delete/'''+str(m.id)+'''">x</a>
                </span></div>'''

        return HttpResponse(json.dumps({'data': res}))

def delete_message(request, id, id_chat):
    Message.objects.filter(id=id).delete()
    return redirect('/chat/' + str(id_chat))

@csrf_exempt
def ajax_add_audio(request):
    '''chat_id = request.POST['chat']
    audio = request.POST['audio']
    filename = request.POST['filename']
    file_data = audio.split(';base64,')[1]

    user = request.session['user']
    user = User.objects.filter(login=user).first()
    m = Message()
    m.file.save(filename, ContentFile(base64.b64decode(file_data)))
    m.chat = Chat.objects.filter(id=chat_id).first()
    m.user = user
    m.text = ' '
    m.save()'''
    audio = request.POST['audio']
    filename = request.POST['filename']
    file_data = audio.split(';base64,')[1]

    chat_id = request.POST['chat']
    user = request.session['user']
    chat = Chat.objects.filter(id=chat_id).first()
    user = User.objects.filter(login=user).first()
    m = Message()
    m.chat = chat
    m.user = user
    m.text = ''
    m.file.save(filename, ContentFile(base64.b64decode(file_data)))
    m.save()

    res = '''<div class ="message bg-secondary-subtle" ><span class ="user" >''' + user.login + '''</span><span class ="text" ><i>  </i></span>'''

    res += '<audio id="audioOlayback" controls style="display: block" src="/media/'+str(m.file)+'"></audio>'

    if user.login == request.session['user']:
        res += '''<span style="color: red">

                       <a style="color: red" href="/delete/''' + str(m.id) + '''">x</a>
                   </span></div>'''



    return HttpResponse(json.dumps({'data': res}))

def update_chat(request):
    if request.method == 'POST':
        data = request.POST
        chat = Chat.objects.filter(id=data['id_chat']).first()
        chat.title = data['title']
        chat.description = data['description']
        path = ''
        if 'avatar' in request.FILES:
            img = request.FILES['avatar']
            f = FileSystemStorage()
            try:
                f.save('avatars_chat/' + img.name, img)
            except:
                pass
            path = 'avatars_chat/' + img.name

        if path != '':
            chat.avatar = path
        ids = [] #список id пользователей добавленых в чат
        for user in data.getlist('users'):
            chat.users.add(int(user)) #'1' => 1
            ids.append(int(user))

        users = User.objects.all()
        for i in users:
            if i.id not in ids:
                chat.users.remove(i.id)



        chat.save()
        return redirect(f'/chat/{data['id_chat']}')



#kivy

#api