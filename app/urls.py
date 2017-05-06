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
    url(r'^documentos/(?P<documento_id>\d+)/deletar/$', views.documento_deletar, name='documento_deletar'),
    url(r'^documentos/(?P<documento_id>\d+)/script/$', views.script_documento, name='script_documento'),
    url(r'^documentos/(?P<documento_id>\d+)/diagrama/$', views.diagrama_documento, name='diagrama_documento'),
    url(r'^documentos/(?P<documento_id>\d+)/relacionamentos/$', views.gerenciar_relacionamentos, name='gerenciar_relacionamentos'),

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
    url(r'^ajax_get_tabelas/(?P<tabela_id>\d+)/$', views.ajax_get_tabelas, name='ajax_get_tabelas'),
    url(r'^ajax_get_chaves/(?P<tabela_id>\d+)/$', views.ajax_get_chaves, name='ajax_get_campos'),
    url(r'^ajax_gerenciar_relacionamentos/$', views.ajax_gerenciar_relacionamentos, name='ajax_gerenciar_relacionamentos'),

    #grupo
    url(r'^grupos/$', views.grupos, name='grupos'),
    url(r'^grupos/(?P<grupo_id>\d+)/$', views.grupo, name='grupo'),
    url(r'^grupos/registrar/$', views.grupo_registrar, name='grupo_registrar'),
    url(r'^grupos/(?P<grupo_id>\d+)/usuario/$', views.grupo_adicionar_usuario, name='grupo_adicionar_usuario'),
    url(r'^grupos/convite/$', views.grupo_convite, name='grupo_convite'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
