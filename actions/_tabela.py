from app.models import *
from classes.util_tabela import *
from classes.util import *


def run_tabela(tabela_id):

    tabela = Tabela.objects.get(id=tabela_id)
    tabela.campos = listar_campos_tabela(tabela, False)
    tabela.primarias = listar_chaves_tabela(tabela, 'PK')
    tabela.estrangeiras = listar_chaves_tabela(tabela, 'FK')

    array_tipo_campo = get_array_tipos_campo()
    array_tipo_chave = get_array_tipos_chave()

    return {'tabela': tabela, 'tipos_campo': array_tipo_campo, 'tipos_chave': array_tipo_chave}