"""samplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.static import serve as media_serve
from django.views.decorators.cache import never_cache

from bboard.views import index

urlpatterns = [
    path('social/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_confirmed.html'), name='password_reset_complete'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(#выполнение сброса пароля
        template_name='registration/confirm_password.html'),#форма для ввода емаила 
        name='password_reset_confirm'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(#отправка успешно
        template_name='registration/email_sent.html'),#форма для ввода емаила 
        name='password_reset_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(#отправка письма для сброса пароля
        template_name='registration/reset_password.html',#форма для ввода емаила 
        subject_template_name='registration/reset_subject.html',#шаблон темы эл письма
        email_template_name='registration/reset_email.html'),#шаблон тела эл письма
        name='password_reset'),
    path('accounts/login/', LoginView.as_view(), name='login'),#вход(аутентификация)
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(
            template_name='registration/password_changed.html'),
            name='password_change_done'),
    path('accounts/password_change', PasswordChangeView.as_view(
        template_name='registration/change_password.html'), 
        name='password_change'),#сменить пароль
    path('accounts/logout/',
    LogoutView.as_view(next_page='index'), name='logout'),#реализуем выход()
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),
]#функция include возвращает вложенный список маршрутов

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#Маршрут для выгрузки файлов
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))

if not settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', serve, {'insecure': True}))
    urlpatterns.append(path('media/<path:path>', media_serve, {'document_root': settings.MEDIA_ROOT}))