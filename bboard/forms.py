#форма для создания новых объявлений
import re
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields
from django.forms import modelform_factory, DecimalField
from django.forms import widgets, modelformset_factory
from django.forms.formsets import formset_factory
from django.forms.widgets import Select
from captcha.fields import CaptchaField

from .models import Bb, Rubric, User, Img, AnyFile


class BbForm(forms.ModelForm):#полное объявление всех полей
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание',
            validators=[validators.RegexValidator(regex='^.{4,}$')],
            error_messages={'invalid': 'Неправильное название товара'},
            widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
            label='Рубрика', help_text='Не забудьте задать рубрику!',
            widget=forms.widgets.Select(attrs={'size': 8}))
    captcha = CaptchaField()
    

    def clean_title(self):#свой валидатор
        val = self.cleaned_data['title']
        if val =='Прошлогодний снег':
            raise ValidationError('Прошлогоднй снег продавать не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара пожалуйста')
        if self.cleaned_data['price'] <0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены пожалуйста')
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
        #labels={'title': 'Название товара'}#можно объявить не полностью частично(полное в приоритете вывода)


'''class BbForm(ModelForm):#создание формы по средствам быстрого объявления(Meta)
    class Meta:
        model = Bb#класс модели с которой связана форма(атрибут класса model)
        fields = ('title', 'content', 'price', 'rubric')#именна полей
        labels={'title': 'Название товара'},
        help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
        field_classes={'price': DecimalField},
        widgets={'rubric': Select(attrs={'size': 8})}'''


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    

'''BbForm = modelform_factory(Bb,
fields=('title','content', 'price', 'rubric'),
labels={'title': 'Название товара'},
help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
field_classes={'price': DecimalField},
widgets={'rubric': Select(attrs={'size': 8})})
#создание формы по средствам фабрики классов, если не нужно в долгосрочной работе'''

RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_order=True, can_delete=True)


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')


class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение', 
        validators=[validators.FileExtensionValidator(
            allowed_extensions=('gif', 'jpg', 'png'))],
            error_messages={'invalid_extension': 'Этот формат файлов не поддерживается'})
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'


class AnyFileForm(forms.ModelForm):
    any_file = forms.ImageField(label='Файл', 
        validators=[validators.FileExtensionValidator(
            allowed_extensions=('gif', 'jpg', 'png', 'doc'))],
            error_messages={'invalid_extension': 'Этот формат файлов не поддерживается'})
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
    archive = forms.ImageField(label='Файл архив', 
        validators=[validators.FileExtensionValidator(
            allowed_extensions=('gif', 'jpg', 'png', 'doc'))],
            error_messages={'invalid_extension': 'Этот формат файлов не поддерживается'})


    class Meta:
        model = AnyFile
        fields = '__all__'
    