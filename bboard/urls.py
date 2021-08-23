#маршруты приложения
from django.urls import path

from .views import index, by_rubric, add_and_save,index_kwarg, rubrics, search, formset_processing, BBcodeTest#импорт контроллер-функций для выполнения по заданному запросу
from .views import BbCreateView,  BbindexView, BBDetailView, BbByRubricView, BbAddView, BbEditView, BbdeliteView, BbRedirectView, UserCreateView#импорт контроллера класса
from .views import RubricFormsetView

urlpatterns = [
    path('BBCode_test/', BBcodeTest),
    path('formset_processing/', formset_processing),
    path('search_rubric/', search),
    path('detail/<int:pk>/', BBDetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),#полная инфа про объявления
    path('index_kwarg/', index_kwarg),#сообщение, тест простых инструментов
    path('rubricview/<int:rubric_id>/', BbByRubricView.as_view()),#рубрика через класс
    path('add_user/', UserCreateView.as_view()),
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