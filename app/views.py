from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_ajax.decorators import ajax

from .models import *
from .forms import TableForm, FieldForm

import json

#meus modulos
from actions._index import run_index
from actions._tabelas import run_tabelas
from actions._tabela import run_tabela
from actions._add_tabela import runAdd_tabela
from actions._add_campo import runAdd_campo
from actions._documentos import run_documentos
from actions._documento import run_documento
from actions._normalizar import run_normalizar
from actions._ajax_add_tabela import run_ajax_add_tabela
from actions._add_documento import run_add_documento
from actions._normalizar_documento import run_normalizar_documento
from actions._ajax_add_campo import run_ajax_add_campo
from actions._ajax_renomear_tabela import run_ajax_renomear_tabela
from actions._ajax_tabela import run_ajax_tabela
from actions._grupo_registrar import run_grupo_registrar
from actions._grupos import run_grupos
from actions._grupo import run_grupo
from actions._grupo_adicionar_usuario import run_grupo_adicionar_usuario
from actions._grupo_convite import run_grupo_convite
from actions._script_documento import run_script_documento
from actions._diagrama_documento import run_diagrama_documento
from actions._documento_deletar import run_documento_deletar
from actions._ajax_get_tabelas import run_ajax_get_tabelas
from actions._ajax_get_chaves import run_ajax_get_chaves
from actions._ajax_compartilhar_documento import run_ajax_compartilhar_documento
from actions._inserir_dados_exemplo import run_inserir_dados_exemplo
from actions._ajax_dados_exemplo import run_ajax_dados_exemplo

from classes.util import *


def index(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_index(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/index.html', context)


def tabelas(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_tabelas(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/tabelas.html', context)


def tabela(request, table_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_tabela(request, table_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/tabela.html', context)


def add_tabela(request):
    """if request.method != 'POST':
        form = TableForm()
    else:
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:tabelas'))

    context = {'form': form}
    """
    context = runAdd_tabela(request)
    if context:
        return render(request, 'app/add_tabela.html', context)
    else:
        return HttpResponseRedirect(reverse('app:tabelas'))


def add_campo(request, table_id):
    context = runAdd_campo(request, table_id)
    if context:
        return render(request, 'app/add_campo.html', context)
    else:
        return HttpResponseRedirect(reverse('app:tabela', args=[table_id]))


def documentos(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_documentos(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/documentos.html', context)


def documento(request, documento_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_documento(documento_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    if context.get('renomear_tabelas', False):
        return render(request, 'app/renomear_tabelas.html', context)

    return render(request, 'app/documento.html', context)


def add_documento(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_add_documento(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    if context['resultado']:
        if request.method == 'POST':
            return HttpResponseRedirect(reverse('app:documentos'))
        elif request.method == 'GET':
            return render(request, 'app/add_documento.html', context)
    else:
        return HttpResponseRedirect(reverse('app:documentos'))


@ajax
def documento_deletar(request, documento_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_documento_deletar(request, documento_id)
    #context['usuario'] = get_usuario(request.session['usuario_id'])

    return HttpResponse(json.dumps(context), content_type="application/json")


def script_documento(request, documento_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_script_documento(request, documento_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/script_documento.html', context)


def diagrama_documento(request, documento_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_diagrama_documento(request, documento_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/diagrama_documento.html', context)


def inserir_dados_exemplo(request, documento_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_inserir_dados_exemplo(request, documento_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/inserir_dados_exemplo.html', context)


@ajax
def ajax_dados_exemplo(request):
    context = run_ajax_dados_exemplo(request)

    return HttpResponse(json.dumps(context), content_type="application/json")


def normalizar_documento(request, documento_id=0):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_normalizar_documento(request, documento_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    if request.method == 'GET':

        if context.get('renomear_tabelas', False):
            response = render(request, 'app/renomear_tabelas.html', context)
        else:
            fn = context.get('fn', None)

            if fn == 0:
                response = render(request, 'app/forma_normal_1.html', context)
            elif fn == 1:
                response = render(request, 'app/forma_normal_2.html', context)
            elif fn == 2:
                    response = render(request, 'app/forma_normal_3.html', context)
            else:
                response = HttpResponseRedirect(reverse('app:documento', args=[documento_id]))#render(request, 'app/normalizar.html', context)

        return response
    else:
        context = {'post': request.POST}
        #return render(request, 'app/mostrar_post.html', context)
        return HttpResponseRedirect(reverse('app:documento', args=[documento_id]))
        #return render(request, reverse('normalizar', kwargs{'documento_id':documento_id}), context)


@ajax
def ajax_add_tabela(request):
    nomes_cookie = request.COOKIES.get('tabelas', '')
    nomes = nomes_cookie.split('666')

    if request.POST['nome'].lower() in nomes:
        context = {'erro': 1}
        response = render(request, 'app/ajax_add_tabela.html', context)
    else:
        context = run_ajax_add_tabela(request)

        tabela = context.get('tabela', '')
        response = render(request, 'app/ajax_add_tabela.html', context)
        #response.COOKIES['tabelas'] = 'teste'

    return response


@ajax
def ajax_add_campo(request):
    context = run_ajax_add_campo(request)
    return render(request, 'app/ajax_add_campo.html', context)


@ajax
def ajax_renomear_tabela(request):
    context = run_ajax_renomear_tabela(request)
    return render(request, 'app/ajax_renomear_tabela.html', context)


@ajax
def ajax_tabela(request, tabela_id):
    context = run_ajax_tabela(request)
    return render(request, 'app/ajax_tabela.html', context)


@ajax
def ajax_get_tabelas(request, tabela_id):
    context = run_ajax_get_tabelas(request, tabela_id)

    return HttpResponse(json.dumps(context), content_type='application/json')


@ajax
def ajax_get_chaves(request, tabela_id):
    context = run_ajax_get_chaves(request, tabela_id)

    return HttpResponse(json.dumps(context), content_type='application/json')


@ajax
def ajax_compartilhar_documento(request):
    context = run_ajax_compartilhar_documento(request)

    return HttpResponse(json.dumps(context), content_type='application/json')


"""
    GRUPO
"""
def grupos(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_grupos(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/grupos.html', context)


def grupo(request, grupo_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_grupo(request, grupo_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    return render(request, 'app/grupo.html', context)


def grupo_registrar(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_grupo_registrar(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    if context['resultado']:
        if request.method == 'POST':
            return HttpResponseRedirect(reverse('app:grupos'))
        else:
            return render(request, 'app/grupo_registrar.html', context)
    else:
        return render(request, 'app/grupo_registrar.html', context)


def grupo_adicionar_usuario(request, grupo_id):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_grupo_adicionar_usuario(request, grupo_id)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    if context['resultado']:
        if request.method == 'GET':
            return render(request, 'app/grupo_adicionar_usuario.html', context)

        if request.method == 'POST':
            return HttpResponseRedirect(reverse('app:grupo', args=[grupo_id]))
    else:
        if request.method == 'POST':
            context['erro'] = 'Erro ao tentar enviar a solicitação<br>Verifique se o email está correto!'

            return render(request, 'app/grupo_adicionar_usuario.html', context)


def grupo_convite(request):
    if not verificar_sessao(request): return redirecionar_login()
    context = run_grupo_convite(request)
    context['usuario'] = get_usuario(request.session['usuario_id'])

    if context['resultado']:
        return HttpResponseRedirect(reverse('app:index'))