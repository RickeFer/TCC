from app.models import *
import pprint


def run_documento(document_id):
    documento = Document.objects.get(id=document_id)

    tabela_base = documento.table_set.get(name=documento.name)
    campos_sem_tabela = tabela_base.field_set.order_by('order')

    tabelas = documento.table_set.order_by('name').exclude(name=documento.name)
    for tabela in tabelas:
        campos = tabela.field_set.order_by('order')
        tabela.campos = campos

    return {'documento': documento, 'base': tabela_base, 'sem_tabela': campos_sem_tabela, 'tabelas': tabelas}