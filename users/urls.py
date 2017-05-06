from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^registrar/$', views.registrar, name='registrar'),
    url(r'^sair/$', views.sair, name='sair'),
]