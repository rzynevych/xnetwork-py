from rest_framework import serializers
from .models import Post, Message, Chat

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'sender_id', 'sender_name', 'text', 'date']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender_id', 'receiver_id', 'sender_name', 'text', 'date']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user_id1', 'user_id2', 'username1', 'username2', 'last_use']