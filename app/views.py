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
    return render(request, 'app/normalizar.html', context)


def normalizar_documento(request, documento_id=0):
    context = run_normalizar_documento()
    return render(request, 'app/')

def mostrar_post(request):
    aux = request.POST
    #define as tabelas
    tabs = []; maior = 0
    for p in aux:
        if p[:6] == 'tabela':
            nome = p[7:]
            temp = {'nome': nome, 'ordem': -1, 'bottom': -1}
            temp['top'] = request.POST[nome + "_top"]
            tabs.append(temp)
            if float(temp['top']) > maior:
                maior = float(temp['top'])
    #define a ordem das tabelas
    cont = 0; temp = []
    while cont < len(tabs):
        for tab in tabs:
            if float(tab['top']) == maior:
                tab['ordem'] = cont
                cont += 1
                temp.append(tab)
                break

        maior = 0
        for tab in tabs:
            if float(tab['top']) > maior and tab['ordem'] == -1:
                maior = float(tab['top'])
    tabs = temp

    tops = []
    for p in aux:
        temp = p.split("'")
        if 'top' in temp:
            #print(aux[p])
            temp = {'tipo': 'campo', 'nome': p, 'top': aux[p]}
            tops.append(temp)
    #fecha o range da tabela
    for i in reversed(range(len(tabs))):
        if i == 0:
            continue
        tabs[i]['bottom'] = tabs[i-1]['top']

    #distribui os campos em suas tabelas
    for tab in tabs:
        temp = []
        for camp in tops:
            if int(camp['top']) >= int(tab['top']):
                if int(tab['bottom']) == -1:
                    temp.append(camp)
                elif int(camp['top']) <= int(tab['bottom']):
                    temp.append(camp)
        tab['campos'] = temp

    for tab in tabs:
        if tab['campos']:
            aux = Table.objects.get(name=tab['nome'])
            for c in tab['campos']:
                nome = c['nome'].split('[')
                campo = Field.objects.get(name=nome[0])
                campo.table = aux
                campo.save()


    context = {'post': request.POST, 'tabelas': tabs, 'tops': tops}
    return render(request, 'app/mostrar_post.html', context)


@ajax
def ajax_add_tabela(request):
    context = run_ajax_add_tabela(request)
    return render(request, 'app/ajax_add_tabela.html', context)