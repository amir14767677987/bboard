from django.core import validators
from django.db import models
from django.apps import AppConfig
from django.contrib.auth.models import Group, Permission




def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное', code='odd',
                              params={'value': val})


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введённое число должно'
                  'находиться в диапазоне от %(min)s до %(max)s',
                  code='out_of_range',
                  params={'min': self.min_value, 'max': self.max_value})


class RubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('order', 'name')

    def order_by_bb_count(self):
        return super().get_queryset().annotate(
            cnt=models.Count('bb')).order_by('-cnt')


class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(
            cnt=models.Count('bb')).order_by('-cnt')


class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    order = models.SmallIntegerField(default=0, db_index=True)

    objects = RubricManager()


    def __str__(self):
        return f'{self.name}'

    # def get_absolut_url(self):
    #     return f"{self.pk}/"

    # def save(self, *args, **kwargs):
    #     # Действия перед сохранением
    #     super().save(*args, **kwargs)
    #     # Действия после сохранением
    #
    # def delete(self, *args, **kwargs):
    #     super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')


class Bb(models.Model):
    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    KINDS = (
        (None, 'Выберите тип публикуемого объявления'),
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )

    # KINDS = (
    #     ('Купля-продажа', (
    #         ('b', 'Куплю'),
    #         ('s', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     ))
    # )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
        # related_name='entries',  # вместо bb_set
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators=[validators.RegexValidator(regex='^.{4,}$')],
        error_messages={'invalid': 'Введите 4 и более символа'},
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    # price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Цена',
        validators=[validate_even]
    )



    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    # is_active = models.BooleanField()
    # email = models.EmailField()
    # url = models.URLField()
    # slug = models.SlugField()

    object = models.Manager()
    by_price = BbManager()

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f} тг.)'
        return self.title

    title_and_price.short_description = 'Название и цена'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание товара')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неоьрицательное'
                                              'значение цены')
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.title} ({self.price} тг.)'

    class Meta:
        ordering = ['-published', 'title']
        # order_with_respect_to = 'rubric'

        unique_together = ('title', 'published')
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

from django.db import models


class IceCream(models.Model):
    FLAVORS = [
        ('vanilla', 'Ванильное'),
        ('chocolate', 'Шоколадное'),
        ('strawberry', 'Клубничное'),
        ('mint', 'Мятное'),
    ]

    flavor = models.CharField(max_length=20, choices=FLAVORS)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.flavor} ({self.size}) - {self.price} руб."




class YourAppConfig(AppConfig):
    name = 'your_app_name'

    def ready(self):
        group, created = Group.objects.get_or_create(name='FullAccessGroup')

        permissions = Permission.objects.all()

        for permission in permissions:
            group.permissions.add(permission)

        print(f'Группа {group.name} создана с правами: {permissions.count()}')




class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

