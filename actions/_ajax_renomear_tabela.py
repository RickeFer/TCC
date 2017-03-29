from app.models import *


def run_ajax_renomear_tabela(request):
    if request.method == 'POST':
        codigo_tabela = request.POST['tabela']
        nome = request.POST['nome'].title()

        tabela = Tabela.objects.get(id=codigo_tabela)

        tabelas = Tabela.objects.filter(documento=tabela.documento.id)

        continuar = True
        for temp in tabelas:
            if temp.nome == nome:
                continuar = False

        if continuar:
            tabela.nome = nome
            tabela.renomear = False
            tabela.save()