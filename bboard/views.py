'''Файл для описания контролера для приложения Bboard'''
import re
from django import template
from django.contrib.auth.views import redirect_to_login
from django.core import paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.http import response
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView#контроллер класса шаблонаBbCreatView
from django.urls import reverse_lazy#функция принимает имя маршрута-результат готовый интернет адрес
from django.views.generic.base import RedirectView, TemplateView#базовый класс
from django.views.generic.detail import DetailView, SingleObjectMixin#более высокоуровневый, обобщенный класс
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, DateDetailView
from django.core.paginator import Paginator
from django.forms import modelformset_factory, BaseModelFormSet, formset_factory
from django.forms.formsets import ORDERING_FIELD_NAME, formset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from precise_bbcode.bbcode import get_parser
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .models import BBCodeModel, Bb, Img, AnyFile#импортируем из моделей класс модели(поля для таблицы)
from .models import Rubric#класс Рубрик
from .forms import BbForm, RegisterUserForm, RubricFormSet, SearchForm, AnyFileForm, ImgForm#класс формы
from .serializers import RubricSerializer

@cache_page(60 * 5)
def by_rubric(request, rubric_id):#котролер для разбиения по рубрикам
    bbs = Bb.objects.filter(rubric=rubric_id)#отбор всех экземпляров класса Бб по рубрике =id
    rubrics = Rubric.objects.all()#все рубрики
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context ={'bbs': bbs, 'rubrics':rubrics,
    'current_rubric': current_rubric}#поля шаблона связаны с переменными
    return render(request, 'bboard/by_rubric.html', context)

@vary_on_headers('User-Agent')
def index(request):
    '''s = 'Список объявлений\r\n\r\n\r\n'
    for bb in Bb.objects.order_by('-published'):
        s+=bb.title+'\r\n'+bb.content+'\r\n\r\n'
    return HttpResponse(s,content_type='text/plain; charset=utf-8')'''#формируем реквест

    '''template = loader.get_template('bboard/index.html')#рендеренг шаблонов, сначало загружаем шаблон путь-строка  
    bbs = Bb.objects.order_by('-published')#значения
    context = {'bbs': bbs}#контекст шаблона(объяние переменной с названием шаблона)
    return HttpResponse(template.render(context, request))'''#низкоуровневые инструменты, делаем рендер

    bbs = Bb.objects.all()#больше не нужно сортировать, сортировка уже в метаклассе модели (классBb)
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 2)#добавим пагинатор
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    if 'counter' in request.session:
        cnt = request.session['counter']+1
    else:
        cnt = 1
    request.session['counter'] = cnt
    context = {'bbs': page.object_list, 'rubrics': rubrics, 'page': page, 'cnt': request.session['counter']}#дополним вывод рубрик
    return render(request, 'bboard/index.html', context)#

'''def add(request):#создание формы и вывод на экран страницы добавлнеия
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/create.html', context)

def add_save(request):#сохраниение нового объявления. Проверка на правильность(isvalid) потом переход на страницу рубрики
    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)'''

def add_and_save (request):#функция выводит форму, создающая и добавляющая объявления
    if request.method == 'POST':#если запрос метода ПОСТ значит произошла отсылка введенных в форму данных
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect (reverse('by_rubric', 
            kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:#повторный вывод формы
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)

def index_kwarg(request):
    resp = HttpResponse("Здесь будет", content_type='text/plain; charset=utf-8')
    resp.write(' главная')
    resp.writelines((' страница', ' сайта'))
    resp['keywords'] = 'Python, Django'
    return resp


@login_required#декларативная авторизация
@permission_required(('bboard.add_rubric'))
def rubrics(request):#упорядочивание рубрик и удаление(нет)
    RubricFormSet = modelformset_factory(Rubric, fields=('name',), 
                    can_order=True, 
                    can_delete=True,
                    formset=RubricBaseFormSet)
        
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()    
            return redirect('index') 
    else:
        formset=RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)
        #return HttpResponseForbidden('Вы не имеете допуска к списку рубрик')
        #return redirect_to_login(reverse('rubrics'))


def BBcodeTest(request):
    bbs = BBCodeModel.objects.all()#
    context = {'bbs':bbs}#
    return render(request, 'bboard/BBCode_test.html', context)#

class BbCreateView(SuccessMessageMixin, CreateView):#контроллер класс формы
    template_name = 'bboard/create.html'#путь к файлу шаблона (страница с формой)
    form_class = BbForm#класс формы связанной с моделью
    success_url = reverse_lazy('index')#адрес перенаправляющий в случае успешной сохранении формы
    success_message = 'Объявление о продаже товара "%(title)s" создано'

    def get_context_data(self, **kwargs):#нужно добавить в контекст шаблона список рубрик
        context = super().get_context_data(**kwargs)#метод формируент контекст шаблона
        context['rubrics'] = Rubric.objects.all()#добавим рубрики
        return context


class UserCreateView(CreateView):
    template_name = 'bboard/create_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):#нужно добавить в контекст шаблона список рубрик
        context = super().get_context_data(**kwargs)#метод формируент контекст шаблона
        context['rubrics'] = Rubric.objects.all()#добавим рубрики
        return context


class BbindexView(ArchiveIndexView):#вывод страницы с помощью  базового контроллер класса templetView класса
    model = Bb
    date_field = 'published'#добавим даты
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    date_list_period = 'day'
    alow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        return context


class BBDetailView(DetailView):#сведения о выбранном объявлении(код очень компактен), добавим дату 
    model = Bb

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


'''class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'#ссылка на шаблон
    context_object_name = 'bbs'#переменная в которой хранятся все нужные записи

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(
            pk=self.kwargs['rubric_id'])
        return context'''


class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'#ссылка на шаблон
    pk_url_kwarg = 'rubric_id'

    def get(self , request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.bb_set_all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['current_rubric'] =self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context

    
class BbAddView(LoginRequiredMixin, FormView):#низкоуровневый класс FormView, только для вошедших(LoginRequiredMixin,)
    template_name = 'bboard/create.html'#путь к файлу шаблона (страница с формой)
    form_class = BbForm#класс формы связанной с моделью
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):#проверка на валидность
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):#создает и возвращает экземпляр формы указанной в form_class. 
        self.object=super().get_form(form_class)#Ее мы сохраняем потому что нужно вернуть pk у объекта для формирования ссылки после сохранения формы
        return self.object# сохраняем форму в атрибуте object

    def get_success_url(self):
        return reverse('by_rubric',
        kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})#1 сылка без bboard:!!!! формирование ссылки на стр в случае верной формы


class RubricFormsetView(FormView):#форма связанная с моделью. добавить рубрику
    template_name = 'bboard/rubric_form.html'
    formset = RubricFormSet(initial=[{'name': 'Новая рубрика'},
                            {'name': 'Еще одна новая рубрика'}],
                            queryset=Rubric.objects.all()[0:5])
    form_class = RubricFormSet


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):#проверка на валидность
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):#создает и возвращает экземпляр формы указанной в form_class. 
        self.object=super().get_form(form_class)#Ее мы сохраняем потому что нужно вернуть pk у объекта для формирования ссылки после сохранения формы
        return self.object# сохраняем форму в атрибуте object

    def get_success_url(self):
        return reverse('index')

class BbEditView(UpdateView):#Класс для редактирования записей
    model = Bb
    form_class = BbForm
    success_url = '/bboard/detail/{id}'#в книге ошибка

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbdeliteView(DeleteView):#класс удаления
    model = Bb
    success_url = '/bboard/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    
class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d'


class RubricBaseFormSet(BaseModelFormSet):#валидация в наборах форм
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms
                if 'name' in form.cleaned_data]
        if ('Недвижимость' not in names) or ('Транспорт' not in names) or ('Мебель' not in names):
            raise ValidationError('Добавьте рубрики недвижимости транспорта и мебели')


def search(request):
    if request.method == 'POST':
        formset = SearchForm(request.POST)
        if formset.is_valid():
            keyword = formset.cleaned_data['keyword']
            rubric_id = formset.cleaned_data['rubric'].pk
            bbs = Bs.objects.filter(...)
            context = {'bbs': bbs}
            return render(request, 'bboard/search_result.html', context)
    else:
        formset = SearchForm()
    context = {'form': formset}
    return render(request, ' bboard/search_r.html', context)


def formset_processing(request):
    FS = formset_factory(SearchForm, extra=3, can_order=True, can_delete=True)

    if request.method =='POST':
        formset = FS(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    keyword = form.cleaned_data['keyword']
                    rubric_id = form.cleaned_data['ORDER']
                    return render(request, 'bboard/process_result.html')
    else:
        formset = FS()
    context = {'formset':formset}
    return render(request, 'bboard/formset.html', context)


def addImg(request):#добавить картинку
    if request.method =='POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'bboard/add_file.html', context)


def addAnyFile(request):#добавить файл
    if request.method =='POST':
        form = AnyFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AnyFileForm()
    context = {'form': form}
    return render(request, 'bboard/add_file.html', context)


def AllImg(request):#показатьт все фото
    imgs = Img.objects.all()
    context = {'imgs': imgs}
    return render(request, 'bboard/AllImg.html', context)#


def ImgDelite(request, pk):#удалить фото
    img = Img.objects.get(pk=pk)
    img.img.delete()
    img.delete()
    return redirect('index')


@api_view(['GET', 'POST'])
def api_rubrics(request):
    if request.method == 'GET':
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        #return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_rubric_detail(request, pk):
    rubric = Rubric.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = RubricSerializer(rubrics)
        return Response(serializer.data)
    elif request.method =='PUT' or request.method == 'PATCH':
        serializer = RubricSerializer(rubric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        rubric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)