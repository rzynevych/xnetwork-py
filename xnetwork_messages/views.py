from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Post, Message, Chat
from .serializers import PostSerializer, MessageSerializer, ChatSerializer
from utils.responses import ResponseObject
from xnetwork_users.models import Subscription
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.db.models import Q

class GetPostsApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ids = Subscription.objects.filter(subscriber_id=request.user.id).values('user_id')
        posts = Post.objects.filter(sender_id__in=ids).order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetOwnPostsApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(sender_id = request.user.id).order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UploadPostApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = {
            'sender_id' : request.user.id,
            'sender_name' : request.user.username,
            'text' : request.data['text']
        }
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetChatMessagesApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(chat=request.GET.get('chat_id')).order_by('-id')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetChatListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        chats = Chat.objects.filter(Q(user_id1=user_id) | Q(user_id2=user_id))
        serializer = ChatSerializer(chats, many=True)
        return Response(ResponseObject(True, serializer.data).dict())


class GetChatIdApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):

        user_id1 = request.user.id
        user_id2 = request.GET.get('converser_id')
        chats = Chat.objects.filter((Q(user_id1=user_id1) & Q(user_id2=user_id2))
                                    | (Q(user_id1=user_id2) & Q(user_id2=user_id1))).values('id')
        if (chats.exists()):
            return Response(ResponseObject(True, {'chat_id': chats[0]['id']}).dict())
        else:
            converser = User.objects.get(id=user_id2)
            data = {
                'user_id1': user_id1,
                'user_id2': user_id2,
                'username1': request.user.username,
                'username2': converser.username
            }
            serializer = ChatSerializer(data=data)
            if serializer.is_valid():
                chat = serializer.save()
                return Response(ResponseObject(True, {'chat_id': chat.id}).dict(), 
                                status=status.HTTP_201_CREATED)
        return Response(ResponseObject(False, serializer.errors).dict(), 
                        status=status.HTTP_400_BAD_REQUEST)

class UploadMessageApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        sender_id = request.user.id
        receiver_id = request.data['receiver_id']
        chat_id = request.data['chat_id']
    
        data = {
            'chat' : chat_id,
            'sender_id' : sender_id,
            'receiver_id' : receiver_id,
            'sender_name' : request.user.username,
            'text' : request.data['text']
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()
            message_serializer = MessageSerializer(message)
            return Response(ResponseObject(True, message_serializer.data).dict(), 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)