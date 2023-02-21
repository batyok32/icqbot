from datetime import date, datetime, timedelta
from django.db import models
from django.db.models import Count, F, Value


def now_plus_30():
    return datetime.now() + timedelta(days=30)


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)


class VpnKey(models.Model):
    class MobileTypes(models.TextChoices):
        ANDROID = "ANDROID", "android"
        IOS = "IOS", "ios"

    name = models.CharField(max_length=5, unique=True)
    client = models.ForeignKey(
        Client, blank=True, null=True, on_delete=models.SET_NULL, related_name="vpns"
    )
    time = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True, blank=True)
    finish_date = models.DateField(default=now_plus_30, blank=True)
    mobile = models.CharField(
        max_length=10, choices=MobileTypes.choices, default=MobileTypes.ANDROID
    )
    price = models.IntegerField(default=150)
    paid = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    # objects = VpnKeyQuerySet.as_manager()

    @property
    def remaining_days(self):
        remaining = (self.finish_date - date.today()).days
        return remaining
