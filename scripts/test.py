from xnetwork_messages.models import Message
from xnetwork_users.models import Subscription
from django.db.models import OuterRef, Subquery
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, BooleanField, Q, F
from django.db import connection


def run():
    # users = User.objects.all().order_by('id')
    # Subscription.objects.create(subscriber=users[0], user=users[1])
    # subscriptions = Subscription.objects.all()
    # user = User.objects.get(1)
    users = User.objects.select_related(
        ).filter(
            (Q(subscriptions__user=1) | Q(subscriptions__user=None)) 
            & (Q(back_subscriptions__subscriber=1) | Q(back_subscriptions__subscriber=None))
        ).annotate(
            subscribed=Case(When(subscriptions__id__isnull=False, then=Value(True)), 
                            default=Value(False), output_field=BooleanField()), 
            in_subscriptions=Case(When(back_subscriptions__id__isnull=False, then=Value(True)), 
                                  default=Value(False), output_field=BooleanField())
        ).values('id', 'username', 'subscribed', 'in_subscriptions')
    print(users.query)
    print(users)
    # print(subscriptions.values())
    # print(connection.queries)
