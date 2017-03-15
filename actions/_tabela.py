from app.models import *


def runTabela(table_id):
    tabela = Tabela.objects.get(id=table_id)
    chaves = tabela.campo_set.filter(primary=1).order_by('ordem')
    campos = tabela.campo_set.filter(primary=0).order_by('ordem')

    return {'tabela': tabela, 'campos': campos, 'chaves': chaves}