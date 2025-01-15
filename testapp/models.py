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
    spares = models.ManyToManyField(Spare, through='Kit',
                                    through_fields=('machine', 'spare'))


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()

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


class IceCream(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    flavor = models.CharField(max_length=100, verbose_name="Вкус")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мороженое"
        verbose_name_plural = "Мороженое"





