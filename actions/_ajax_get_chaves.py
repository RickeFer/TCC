from app.models import *
from classes.util_tabela import *


def run_ajax_get_chaves(request, tabela_id):
    tabela = Tabela.objects.get(id=tabela_id)

    chaves = {}
    for chave in listar_chaves_tabela(tabela, 'PK') + listar_chaves_tabela(tabela, 'FK'):
        chaves[chave.id] = chave.nome

    return {'chaves':chaves}