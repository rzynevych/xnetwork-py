from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from utils.responses import ResponseObject
from django.db.models import Case, When, Value, BooleanField, Q
from django.db.models import Exists, OuterRef, Subquery
from .models import Subscription
from .serializers import UserSerializer

class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return Response(ResponseObject(True, None).dict())
        else:
            return Response(ResponseObject(False, None).dict())

class SignUpApiView(APIView):
    # 2. Create user
    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(
            request.data['username'], request.data['email'], request.data['password'])
        user.save()
        response = ResponseObject(True, None)
        return Response(response.dict(), status=status.HTTP_201_CREATED)
    
class AuthCheckApiView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(ResponseObject(True, serializer.data).dict())
        else:
            return Response(ResponseObject(False, None).dict())
    
class GetUsersByQueryApiView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        query = request.GET.get('query', '')
        back_subscription = Subscription.objects.filter(subscriber_id=OuterRef('pk'), user_id=user_id)
        subscription = Subscription.objects.filter(subscriber_id=user_id, user_id=OuterRef('pk'))
        users = User.objects.filter(Q(username__contains=query) & ~Q(id=user_id)).annotate(
            subscribed=Exists(Subquery(back_subscription)), 
            in_subscriptions=Exists(Subquery(subscription))
        ).values('id', 'username', 'subscribed', 'in_subscriptions')

        print(users.query)
        return Response(users)

class AddSubscriptionApiView(APIView):
    def get(self, request, *args, **kwargs):
        subscriber_id = request.user.id
        user_id = request.GET.get('user_id')
        Subscription.objects.create(subscriber_id=subscriber_id, user_id=user_id)
        return Response(ResponseObject(True, None).dict())

class RemoveSubscriptionApiView(APIView):
    def get(self, request, *args, **kwargs):
        subscriber_id = request.user.id
        user_id = request.GET.get('user_id')
        Subscription.objects.filter(subscriber_id=subscriber_id, user_id=user_id).delete()
        return Response(ResponseObject(True, None).dict())