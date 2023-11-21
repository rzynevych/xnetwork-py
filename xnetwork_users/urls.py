from django.urls import path
from .views import (
    LoginApiView,
    SignUpApiView,
    AuthCheckApiView,
    GetUsersByQueryApiView,
    AddSubscriptionApiView,
    RemoveSubscriptionApiView
)

urlpatterns = [
    path('login/', LoginApiView.as_view()),
    path('sign-up/', SignUpApiView.as_view()),
    path('auth-check/', AuthCheckApiView.as_view()),
    path('get-by-query/', GetUsersByQueryApiView.as_view()),
    path('add-subscription/', AddSubscriptionApiView.as_view()),
    path('remove-subscription/', RemoveSubscriptionApiView.as_view()),
]