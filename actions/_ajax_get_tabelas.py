from app.models import *
from classes.util_documento import *


def run_ajax_get_tabelas(request, tabela_id):
    tabela = Tabela.objects.get(id=tabela_id)

    tabelas = {}
    for temp in Tabela.objects.filter(documento=tabela.documento).exclude(id=tabela_id).exclude(nome='tabela_base'):
        tabelas[temp.id] = temp.nome



    return {'tabelas':tabelas}