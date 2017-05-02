from app.models import *
from classes.util_documento import *
from classes.util_tabela import *


def run_documento_deletar(request, documento_id):

    """
        DELETA O DOCUMENTO
            - DELETA AS DEPENDENCIAS
            - DELETA AS RELACOES CAMPO-TABELA
            - DELETA OS CAMPOS
            - DELETA AS TABELAS
            - DELETA O DOCUMENTO
    """
    documento = get_documento_completo(documento_id)

    try:
        for tabela in documento.tabelas:
            dependencias = listar_dependencias(tabela)
            relacoes = listar_relacao_campo(tabela)
            campos = listar_campos_tabela(tabela)

            for dependencia in dependencias:
                dependencia.delete()
            for relacao in relacoes:
                relacao.delete()
            for campo in campos:
                campo.delete()

            tabela.delete()
        documento.delete()

        return {'resultado': True}
    except:
        return {'resultado': False}