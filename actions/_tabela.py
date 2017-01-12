from app.models import *


def runTabela(table_id):
    tabela = Table.objects.get(id=table_id)
    campos = tabela.field_set.order_by('order')
    return {'tabela': tabela, 'campos': campos}