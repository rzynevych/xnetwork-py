from django.db import models

# Create your models here.

class Chat(models.Model):
    user_id1 = models.BigIntegerField()
    user_id2 = models.BigIntegerField()
    username1 = models.CharField(max_length = 64)
    username2 = models.CharField(max_length = 64)
    last_use = models.DateTimeField(auto_now_add = True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_id = models.BigIntegerField()
    receiver_id = models.BigIntegerField()
    sender_name = models.CharField(max_length = 64)
    text = models.CharField(max_length = 300)
    date = models.DateTimeField(auto_now_add = True)

class Post(models.Model):
    sender_id = models.BigIntegerField()
    sender_name = models.CharField(max_length = 64)
    text = models.CharField(max_length = 300)
    date = models.DateTimeField(auto_now_add = True)
