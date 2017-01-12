from app.models import *


def run_documento(document_id):
    documento = Document.objects.get(id=document_id)
    tabelas = documento.table_set.order_by('name')

    return {'documento': documento, 'tabelas': tabelas}