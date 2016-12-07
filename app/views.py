from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django_ajax.decorators import ajax

from .models import *
from .forms import TableForm, FieldForm


def index(request):
    return render(request, 'app/index.html')


def tabelas(request):
    form = TableForm()
    tabelas = Table.objects.all()
    context = {'tabelas': tabelas, 'form': form}
    return render(request, 'app/tabelas.html', context)


def tabela(request, table_id):
    tabela = Table.objects.get(id=table_id)
    campos = tabela.field_set.order_by('order')
    context = {'tabela': tabela, 'campos': campos}
    return render(request, 'app/tabela.html', context)


def add_tabela(request):
    if request.method != 'POST':
        form = TableForm()
    else:
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:tabelas'))

    context = {'form': form}
    return render(request, 'app/add_tabela.html', context)


def add_campo(request, table_id):
    tabela = Table.objects.get(id=table_id)

    if request.method != 'POST':
        form = FieldForm()
    else:
        form = FieldForm(data=request.POST)
        if form.is_valid():
            novo_campo = form.save(commit=False)
            #relaciona tabela
            novo_campo.table = tabela
            ult_campo = tabela.field_set.order_by('order')

            if len(ult_campo):
                ult_campo = ult_campo[len(ult_campo)-1].order
            else:
                ult_campo = -1

            novo_campo.order = ult_campo + 1
            novo_campo.save()
            return HttpResponseRedirect(reverse('app:tabela', args=[table_id]))

    context = {'tabela': tabela, 'form': form}
    return render(request, 'app/add_campo.html', context)

def documentos(request):
    documentos = Document.objects.all()
    print(documentos)
    context = {'documentos': documentos}
    return render(request, 'app/documentos.html', context)

def documento(request, document_id):
    documento = Document.objects.get(id=document_id)
    tabelas = documento.table_set.order_by('name')

    context = {'documento': documento, 'tabelas': tabelas}
    return render(request, 'app/documento.html', context)


def normalizar(request, table_id=0):
    tabela = Table.objects.get(id=table_id)
    campos = tabela.field_set.order_by('order')

    #separa linhas de 8 campos em um dicionario
    if len(campos) > 8:
        dicCampos = {}; aux = []; cont = 0
        for c in campos:
            aux.append(c)
            if c.order%8==0:
                dicCampos[cont] = aux
                aux = []
                cont += 1
        if len(aux):
            dicCampos[cont] = aux
        #campos = dicCampos
    else:
        dicCampos = {campos}
        #campos = dicCampos

    tabelas = Table.objects.all()
    context = {'tabela': tabela, 'tabelas': tabelas, 'dicCampos': dicCampos, 'form': TableForm()}

    return render(request, 'app/normalizar.html', context)

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
    if request.method == 'POST':
        nome = request.POST['nome']
        table = Table()
        table.name = nome
        table.save()

    tabelas = Table.objects.all()
    context = {'tabelas': tabelas}

    if request.POST['pag'] == 'normalizar':
        table_id = request.POST['id']
        tabela = Table.objects.get(id=table_id)
        campos = tabela.field_set.order_by('order')
        form = TableForm()
        # separa linhas de 8 campos em um dicionario
        if len(campos) > 8:
            dicCampos = {};
            aux = [];
            cont = 0
            for c in campos:
                aux.append(c)
                if c.order % 8 == 0:
                    dicCampos[cont] = aux
                    aux = []
                    cont += 1
            if len(aux):
                dicCampos[cont] = aux
                # campos = dicCampos
        else:
            dicCampos = {campos}
            # campos = dicCampos

        context['dicCampos'] = dicCampos
        context['pag'] = 'normalizar'

    return render(request, 'app/ajax_add_tabela.html', context)