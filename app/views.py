from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_ajax.decorators import ajax

from .models import *
from .forms import TableForm, FieldForm

#meus modulos
from actions._tabelas import runTabelas
from actions._tabela import runTabela
from actions._add_tabela import runAdd_tabela
from actions._add_campo import runAdd_campo
from actions._documentos import run_documentos
from actions._documento import run_documento
from actions._normalizar import run_normalizar
from actions._ajax_add_tabela import run_ajax_add_tabela
from actions._add_documento import run_add_documento
from actions._normalizar_documento import run_normalizar_documento
from actions._ajax_add_campo import run_ajax_add_campo


def index(request):
    #run(request)
    return render(request, 'app/index.html')


def tabelas(request):
    context = runTabelas()
    return render(request, 'app/tabelas.html', context)


def tabela(request, table_id):
    context = runTabela(table_id)
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
    context = run_documentos()
    return render(request, 'app/documentos.html', context)


def documento(request, document_id):
    context = run_documento(document_id)
    return render(request, 'app/documento.html', context)


def add_documento(request):
    context = run_add_documento(request)
    if context:
        return render(request, 'app/add_documento.html', context)
    else:
        return HttpResponseRedirect(reverse('app:documentos'))


def normalizar(request, documento_id=0):
    context = run_normalizar(documento_id)
    return render(request, 'app/normalizar2.html', context)


def normalizar_documento(request, documento_id=0):
    context = run_normalizar_documento(request, documento_id)
    if request.method != 'POST':
        nomes = context.get('nomes', None)
        if nomes:
            del context['nomes']
            nomes_min = ''
            for letra in nomes:
                nomes_min += letra.lower()

        response = render(request, 'app/normalizar.html', context)
        response.set_cookie('tabelas', nomes_min.strip(), 3600)

        return response
    else:
        context = {'post': request.POST}
        #return render(request, 'app/mostrar_post.html', context)
        return HttpResponseRedirect(reverse('app:normalizar', args=[documento_id]))
        #return render(request, reverse('normalizar', kwargs{'documento_id':documento_id}), context)


def mostrar_post(request):
    pass


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