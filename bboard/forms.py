from django.core import validators
from django.forms import ModelForm, modelform_factory, Select
from django.forms.fields import  DecimalField
from django import forms
from .models import IceCream, Rubric
from bboard.models import Bb
from django import forms
from captcha.fields import CaptchaField
class BbForm(ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки')
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')


BbForm = modelform_factory(
    Bb,
    fields={'title', 'content', 'price', 'rubric'},
    labels={'title': 'Название товара'},
    help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
    field_classes={'price': DecimalField},
    widgets={'rubric': Select(attrs={'size': 8})}
)

# class BbForm(ModelForm):
#     title = forms.CharField(ladel='Название товара')
#     content = forms.CharField(label='Описание')

# class BbForm(ModelForm):
#     title = forms.CharField(
#         label='Название товара',
#         validators=[validators.RegexValidator(regex='^.{4,}$')],
#         error_massage={}
#     )


from django import forms
from .models import IceCream


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ['flavor', 'size', 'price']


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрик')

class UserForm(forms.Form):
        user_id = forms.IntegerField(label='Введите ID пользователя')




