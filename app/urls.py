from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #url tabelas
    url(r'^tabelas/$', views.tabelas, name='tabelas'),
    url(r'^tabelas/(?P<table_id>\d+)/$', views.tabela, name='tabela'),
    url(r'^add_tabela/$', views.add_tabela, name='add_tabela'),

    #url campos
    url(r'^add_campo/(?P<table_id>\d+)/$', views.add_campo, name='add_campo'),

    #url documentos
    url(r'^documentos/$', views.documentos, name='documentos'),
    url(r'^documentos/(?P<documento_id>\d+)/$', views.documento, name='documento'),
    url(r'^add_documento/$', views.add_documento, name='add_documento'),

    #url normalizar
    #url(r'^normalizar/$', views.normalizar, name='normalizar'),
    #url(r'^normalizar/(?P<table_id>\d+)/$', views.normalizar, name='normalizar'),

    #url normalizar documento
    url(r'^normalizar/(?P<documento_id>\d+)/$', views.normalizar_documento, name='normalizar'),

    #ajax
    url(r'^ajax_add_tabela/$', views.ajax_add_tabela, name='ajax_add_tabela'),
    url(r'^ajax_add_campo/$', views.ajax_add_campo, name='ajax_add_campo'),
    url(r'^ajax_renomear_tabela/$', views.ajax_renomear_tabela, name='ajax_renomear_tabela'),
    url(r'^ajax_tabela/(?P<tabela_id>\d+)/$', views.ajax_tabela, name='ajax_tabela'),

    #url(r'^mostrar_post/$', views.mostrar_post, name='mostrar_post'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
