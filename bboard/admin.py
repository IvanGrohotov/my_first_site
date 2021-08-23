from django.contrib import admin

from .models import Bb
from .models import Rubric
from .models import BBCodeModel

class BbAdmin(admin.ModelAdmin):#редактор модели-красивое представление таблицы т.е шапка и полей на САЙТЕ АДМИНА
    list_display = ('title', 'content','price', 'published', 'rubric')#поля кот показываем, добавим рубрики
    list_display_links = ('title', 'content')#имена полей которые  преобразуются гиперссылку
    search_fields = ('title', 'content',)#поля по которым производится поиск

admin.site.register(Bb, BbAdmin)#регистрация модулей на админестративном сайте
admin.site.register(Rubric)
admin.site.register(BBCodeModel)
