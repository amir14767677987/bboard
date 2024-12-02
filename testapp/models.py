from django.db import models
from django.contrib.auth.models import User
from django.views.generic import ListView


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30)

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)

from django.db import models

class SMS(models.Model):
    sms_id = models.CharField(max_length=100, unique=True)
    sender = models.CharField(max_length=100)
    text = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"SMS от {self.sender}: {self.text[:30]}"

    class SMSListView(ListView):
        template_name = 'testapp/sms_list.html'
        context_object_name = 'sms_list'
        ordering = ['-received_at']




