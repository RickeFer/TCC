from app.models import *


def run_ajax_add_tabela(request):
    if request.method == 'POST':
        nome = request.POST['nome'].title()
        document = Documento.objects.get(id=request.POST['documento'])
        #verifica se o nome ja existe
        table = Tabela()
        table.nome = nome
        table.documento = document
        table.tabela_tipo = 1
        if request.POST['pag'] == 'tabelas':
            table.save()

    return {'pag': request.POST['pag'], 'tabela': table}