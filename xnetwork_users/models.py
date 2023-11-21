from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='back_subscriptions', on_delete=models.CASCADE)
