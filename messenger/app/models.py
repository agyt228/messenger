from django.db import models

class User(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatars/')
    token = models.CharField(max_length=200, default=None)
class Chat(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    avatar = models.ImageField(upload_to='avatars_chat/', default='/avatars_chat/default.png')
    users = models.ManyToManyField(User, related_name='Users')
    admin_chat = models.ForeignKey(User, on_delete=models.CASCADE)
class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file/', blank=True, null=True)
    data = models.DateTimeField(auto_now=True)
    audio = models.FileField(upload_to='file/', blank=True, null=True)


