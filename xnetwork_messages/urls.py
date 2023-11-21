from django.urls import path
from .views import (
    GetPostsApiView,
    GetOwnPostsApiView,
    UploadPostApiView,
    GetChatIdApiView,
    GetChatListApiView,
    GetChatMessagesApiView,
    UploadMessageApiView
)

urlpatterns = [
    path('get-posts/', GetPostsApiView.as_view()),
    path('get-own-posts/', GetOwnPostsApiView.as_view()),
    path('upload-post/', UploadPostApiView.as_view()),
    path('get-chat-id/', GetChatIdApiView.as_view()),
    path('get-chat-list/', GetChatListApiView.as_view()),
    path('get-chat-messages/', GetChatMessagesApiView.as_view()),
    path('upload-message/', UploadMessageApiView.as_view()),    
]