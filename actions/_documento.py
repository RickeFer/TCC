from app.models import *
import pprint

from classes.util_grupo import *
from classes.util_documento import *


def run_documento(documento_id):
    documento = Documento.objects.get(id=documento_id)

    tabela_base = documento.tabela_set.get(nome='tabela_base', tabela_tipo=0)

    array_campos_sem_tabela = Campo_Tabela.objects.filter(tabela=tabela_base)
    campos_sem_tabela = []
    for rel in array_campos_sem_tabela:
        temp = Campo.objects.get(id=rel.campo.id)
        campos_sem_tabela.append(temp)


    tabelas = documento.tabela_set.order_by('nome').exclude(nome='tabela_base', tabela_tipo=0)
    fn = 3

    if tabelas:
        for tabela in tabelas:
            campos, chaves_primaria, chaves_estrangeiras = [], [], []
            array_campos = tabela.campo_tabela_set.filter(tipo_campo='Normal')
            for rel in array_campos:
                temp = Campo.objects.get(id=rel.campo.id)
                campos.append(temp)

            array_chaves = tabela.campo_tabela_set.filter(tipo_campo='PK')
            for rel in array_chaves:
                temp = Campo.objects.get(id=rel.campo.id)
                chaves_primaria.append(temp)

            array_chaves_estrangeiras = tabela.campo_tabela_set.filter(tipo_campo='FK')
            for rel in array_chaves_estrangeiras:
                temp = Campo.objects.get(id=rel.campo.id)
                chaves_estrangeiras.append(temp)

            tabela.campos = campos
            tabela.chaves = chaves_primaria
            tabela.estrangeiras = chaves_estrangeiras

            if tabela.forma_normal < fn:
                fn = tabela.forma_normal

        tabelas_renomear = listar_tabelas_renomear(documento_id)

        if len(tabelas_renomear):
            documento.tabelas = tabelas_renomear

            return {'renomear_tabelas': True, 'documento': documento}
    else:
        fn = 0

    flag_dados = verificar_dados_documento(documento_id)
    grupos = listar_grupos(documento.grupo.id)


    return {'documento': documento, 'base': tabela_base, 'sem_tabela': campos_sem_tabela, 'tabelas': tabelas, 'fn': fn, 'grupos': grupos, 'flag_dados':flag_dados}