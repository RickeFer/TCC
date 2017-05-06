from classes.util_documento import *


def run_gerenciar_relacionamentos(request, documento_id):

    if request.method == 'GET':
        documento = get_documento_completo(documento_id)

        for tabela in documento.tabelas:
            tabela.chaves = tabela.primarias + tabela.estrangeiras

        return {'documento': documento}

    if request.method == 'POST':
        return {}