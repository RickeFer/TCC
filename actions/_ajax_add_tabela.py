from app.models import *


def run_ajax_add_tabela(request):
    if request.method == 'POST':
        nome = request.POST['nome'].title()
        table = Table()
        table.name = nome
        document = Document.objects.get(id=request.POST['documento'])
        table.document = document
        table.type_table = 1
        if request.POST['pag'] == 'tabelas':
            table.save()

    return {'pag': request.POST['pag'], 'tabela': table}


    """
    tabelas = Table.objects.all()
    context = {'tabelas': tabelas}

    if request.POST['pag'] == 'normalizar':
        table_id = request.POST['id']
        tabela = Table.objects.get(id=table_id)
        campos = tabela.field_set.order_by('order')
        form = TableForm()
        # separa linhas de 8 campos em um dicionario
        if len(campos) > 8:
            dicCampos = {}
            aux = []
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
    """

    return context