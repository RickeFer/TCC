from app.models import *


def runTabela(table_id):
    tabela = Tabela.objects.get(id=table_id)
    chaves = tabela.field_set.filter(primary=1).order_by('order')
    campos = tabela.field_set.filter(primary=0).order_by('order')

    return {'tabela': tabela, 'campos': campos, 'chaves': chaves}