#маршруты приложения
from django.urls import path

from .views import index, by_rubric, add_and_save,index_kwarg, rubrics, search, formset_processing, BBcodeTest, addImg, addAnyFile, AllImg,ImgDelite#импорт контроллер-функций для выполнения по заданному запросу
from .views import BbCreateView,  BbindexView, BBDetailView, BbByRubricView, BbAddView, BbEditView, BbdeliteView, BbRedirectView, UserCreateView#импорт контроллера класса
from .views import RubricFormsetView, api_rubrics, api_rubric_detail

urlpatterns = [
    path('api/rubrics/<int:pk>', api_rubric_detail),
    path('api/rubrics/', api_rubrics),
    path('img_delete/<int:pk>/', ImgDelite, name='img_delete'),
    path('all_img/', AllImg, name='all_img'),
    path('add_file/', addAnyFile, name='add_file'),
    path('add_img/', addImg, name='add_img'),
    path('BBCode_test/', BBcodeTest),
    path('formset_processing/', formset_processing),
    path('search_rubric/', search),
    path('detail/<int:pk>/', BBDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),#полная инфа про объявления
    path('index_kwarg/', index_kwarg),#сообщение, тест простых инструментов
    path('rubricview/<int:rubric_id>/', BbByRubricView.as_view()),#рубрика через класс
    path('add_user/', UserCreateView.as_view(), name='add_user'),
    path('rubrics/', rubrics, name='rubrics'),
    path('rubric_formset/', RubricFormsetView.as_view(), name='rubrics_formset'),
    path('add/', add_and_save, name='add'),#добавление объявления
    path('class_add/',BbAddView.as_view()),#добавление через класс
    path('edit/<int:pk>', BbEditView.as_view(), name='edit'),#редактирование, обязательно передаем pk!!
    path('delite/<int:pk>', BbdeliteView.as_view(), name='delite'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),#рубрика через функцию
    path('indexview/',  BbindexView.as_view()),#главная через класс
    path('', index, name='index'),#главная чрез функцию
]#добавим имена для маршрутов(обратное разрешение интернет запросов). 2. добавим add_save и add