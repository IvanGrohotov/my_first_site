from django.contrib import admin

from .models import Bb
from .models import Rubric
from .models import BBCodeModel, Machine, Spare


class BbInline(admin.StackedInline):
    model = Bb


class RubricAdmine(admin.ModelAdmin):
    inlines = [BbInline]
class BbAdmin(admin.ModelAdmin):#редактор модели-красивое представление таблицы т.е шапка и полей на САЙТЕ АДМИНА
    list_display = ('title', 'content','price', 'published', 'rubric')#поля кот показываем, добавим рубрики
    list_display_links = ('title', 'content')#имена полей которые  преобразуются гиперссылку
    search_fields = ('title', 'content',)#поля по которым производится поиск
    fieldsets = (
        (None, {
            'fields': (('title', 'rubric'), 'content'),
            'classes': ('wide',),
        }),
        ('Дополнительные сведения', {
            'fields': ('price',),
            'description': 'Параметры, необязательные для указания.',
        })
    )


class MachineAdmine(admin.ModelAdmin):
    fields = ('name', )
    filter_horizontal = ('spares',)

admin.site.register(Bb, BbAdmin)#регистрация модулей на админестративном сайте
admin.site.register(Rubric, RubricAdmine)
admin.site.register(BBCodeModel)
admin.site.register(Spare)
admin.site.register(Machine, MachineAdmine)
