from classes.util_documento import *
from classes.util_tabela import *


def run_diagrama_documento(request, documento_id):
    documento = get_documento_completo(documento_id)

    ini = 0

    for tabela in documento.tabelas:
        tabela.relacao = get_relacionamento(tabela)
        tabela.pos = ini
        ini += 150

    return {'documento': documento}