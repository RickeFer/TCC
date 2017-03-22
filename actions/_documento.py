from app.models import *
import pprint


def run_documento(documento_id):
    documento = Documento.objects.get(id=documento_id)

    #tabela_base = documento.tabela_set.get(nome=documento.name)
    tabela_base = documento.tabela_set.get(nome='tabela_base', tabela_tipo=0)

    array_campos_sem_tabela = Campo_Tabela.objects.filter(tabela=tabela_base)
    campos_sem_tabela = []
    for rel in array_campos_sem_tabela:
        temp = Campo.objects.get(id=rel.campo.id)
        campos_sem_tabela.append(temp)
    #campos_sem_tabela = tabela_base.campo_set.order_by('ordem')

    #tabelas = documento.tabela_set.order_by('name').exclude(nome=documento.name)
    tabelas = documento.tabela_set.order_by('nome').exclude(nome='tabela_base', tabela_tipo=0)
    fn = 3
    if tabelas:
        for tabela in tabelas:
            campos = []
            #campos = tabela.campo_set.order_by('ordem')
            array_campos = tabela.campo_tabela_set.all()
            for rel in array_campos:
                temp = Campo.objects.get(id=rel.campo.id)
                campos.append(temp)

            tabela.campos = campos
            if tabela.forma_normal < fn:
                fn = tabela.forma_normal
    else:
        fn = 0


    return {'documento': documento, 'base': tabela_base, 'sem_tabela': campos_sem_tabela, 'tabelas': tabelas, 'fn': fn}