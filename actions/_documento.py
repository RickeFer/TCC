from app.models import *
import pprint


def run_documento(documento_id):
    documento = Documento.objects.get(id=documento_id)

    #tabela_base = documento.tabela_set.get(nome=documento.name)
    tabela_base = documento.tabela_set.get(nome='tabela_base', tabela_tipo=0)
    campos_sem_tabela = tabela_base.campo_set.order_by('ordem')

    #tabelas = documento.tabela_set.order_by('name').exclude(nome=documento.name)
    tabelas = documento.tabela_set.order_by('nome').exclude(nome='tabela_base', tabela_tipo=0)
    fn = 3
    if tabelas:
        for tabela in tabelas:
            campos = tabela.campo_set.order_by('ordem')
            tabela.campos = campos
            if tabela.forma_normal < fn:
                fn = tabela.forma_normal
    else:
        fn = 0


    return {'documento': documento, 'base': tabela_base, 'sem_tabela': campos_sem_tabela, 'tabelas': tabelas, 'fn': fn}