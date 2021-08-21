from django.db import models
from django.contrib.auth.models import User #стандартная модель хранящая сведения о пользовотеле на джанго сайте
from django.core import validators
from django.core.exceptions import ValidationError

def validate_even(val):#свой валидатор
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечетное', code='odd', params={'value': val})

'''class MinMaxValueValidator:#Класс валидатор
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val> self.max_value:
            raise ValidationError('Введенное число должно находиться в диапазоне от %(min)s до %(max)s', 
            code='out_of_range', params={'min': self.min_value, 'max': self.max_value})'''


class Bb(models.Model):#описание полей базы данных (таблица)
    title = models.CharField(max_length=50, verbose_name='Товар', 
            validators=[validators.RegexValidator(regex='^.{4,}$')],
            error_messages={'invalid': 'Неправильное название товара'})#добавим валидатор по регулярному выражению
    content = models.TextField(null=True, blank=True, verbose_name='Описание',)
    price = models.FloatField(null=True, blank=True, verbose_name='Цена',
            validators=[validate_even,])#добавили свой валидатор MinMaxValueValidator(1,999999)
    published = models.DateTimeField(auto_now_add=True,db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, 
    on_delete=models.PROTECT, verbose_name='Рубрика')#еще одно поле рубрика, foreignKey поле Первичной модели, 1-ссылка на класс,2 поле не обяз,3 защита от удаления всех полей рубрики какойлибо

    class Meta:#параметры полей и моделей(представление в человеческом виде-ед и мн число и порядок)
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published','title']#порядок сортировки
        unique_together = (
            ('title', 'published'),
            ('title', 'price', 'rubric')
        )#теперь поля товара и даты должны быть уникальны
        get_latest_by = '-published'
    
    def title_and_price(self):# функция для функционального поля, выводит название и цену или название
        if self.price:
            return '%s (%.2f)' %(self.title, self.price)
        else:
            return self.title
    title_and_price.short_description = 'Название и цена'

    def clean(self):#валидация модели целиком
        errors = {}#словарь ошибок
        if not self.content:#описание обязательно (можно было это сделать в описании поля)
            errors['content'] = ValidationError('Укажите описание продаваемого товара')

        if self.price and self.price <0:#цена не отриц
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        
        if errors:
            raise ValidationError(errors)


class Rubric (models.Model):#клас рубрик
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True)
    
    def __str__(self):#класс представляющий рубрики стоками
        return self.name
    
    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['order', 'name']

class AdvUser(models.Model):#доп описание пользователя
    is_activated = models.BooleanField(default=True)#поле тру фолс
    user = models.OneToOneField(User, on_delete=models.CASCADE)#наследование один-содним

class Spare(models.Model):
    name = models.CharField(max_length=40)

class Machine(models.Model):
    name = models.CharField(max_length=30)     #through='Kit',through_fields=('machine', 'spare')
    spares = models.ManyToManyField(Spare, through='Kit',through_fields=('machine', 'spare'))#наследование многие-со-многими, в ведущей модели указываем связующую

class Kit(models.Model):#связующая модель для добавления дополнительных данных
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)#связь многи-с-многие с вудущей и ведомой моделями
    spare= models.ForeignKey(Spare, on_delete=models.CASCADE)#
    count = models.IntegerField()#поля доп данных'''


class RevRubric(Rubric):#наследование модели способ создания прокси-модели
    class Meta:
        proxy = True
        ordering = ['-name']