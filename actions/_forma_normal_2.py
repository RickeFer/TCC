from app.models import *

from classes.util_tabela import *
from classes.util_documento import *
from classes.util import *


def run_forma_normal_2(request, documento_id):
    documento = Documento.objects.get(id=documento_id)


    if request.method == 'GET':
        documento.tabelas = documento.tabela_set.filter(forma_normal=1)

        for tabela in documento.tabelas:
            tabela.chaves = listar_chaves_tabela(tabela, 'PK') + listar_chaves_tabela(tabela, 'FK')
            tabela.campos = listar_campos_tabela(tabela, False)


        return {'fn':1, 'documento':documento}

    elif request.method == 'POST':
        array_post = request.POST

        tabelas = documento.tabela_set.filter(forma_normal=1)
        for tabela in tabelas:
            tabela.forma_normal = 2
            tabela.save()
            tabela.chaves = listar_chaves_tabela(tabela, 'PK') + listar_chaves_tabela(tabela, 'FK')

        """
            CRIA UM DICIONARIO COM AS TABELAS
        """
        dict_tabelas = {}
        for tabela in tabelas:
            dict_tabelas[tabela.id] = {'chaves':tabela.chaves, 'campos':{}}


        """
            SETA A QUANTIDADE DE DEPENDENCIAS DE CADA CAMPO
        """
        for chave, valor in array_post.items():
            if chave != 'csrfmiddlewaretoken' and chave != 'forma_normal':
                campo_id = chave.split('_')[0]
                campo = Campo.objects.get(id=campo_id)
                rel = campo.campo_tabela_set.get(tipo_campo='Normal')

                if dict_tabelas[rel.tabela.id]['campos'].get(rel.id, 0):
                    dict_tabelas[rel.tabela.id]['campos'][rel.id].append(valor)
                else:
                    dict_tabelas[rel.tabela.id]['campos'][rel.id] = [valor]


        dict_novas_tabelas = {}

        """
            PERCORRE AS TABELAS E VERIFICA SE HA CAMPOS QUE NAO DEPENDEM DA CHAVE INTEIRA
        """
        for tabela_id, dict in dict_tabelas.items():
            quantidade_chaves = len(dict['chaves'])

            for campo, dep in dict['campos'].items():
                if len(dep) < quantidade_chaves:
                    aux = array_2_str(dep)

                    if dict_novas_tabelas.get(aux, False):
                        dict_novas_tabelas[aux]['campos'].append(campo)
                    else:
                        #GERA UMA NOVA TABELA
                        hash = gerar_hash(16)
                        nova_tabela = Tabela(documento=documento, nome=hash, forma_normal=2, renomear=True)

                        dict_novas_tabelas[aux] = {'tabela':nova_tabela, 'campos':[campo]}


        """
            PERCORRE AS NOVAS TABELAS
            SALVA OS CAMPOS EM SUAS TABELAS RESPECTIVAS
            E RELACIONA AS CHAVES
        """
        for chaves, dict in dict_novas_tabelas.items():
            tabela = dict['tabela']
            tabela.save()

            for campo_id in chaves.split('_'):
                campo = Campo.objects.get(id=campo_id)
                rel = campo.campo_tabela_set.get(tipo_campo='PK')
                rel.tipo_campo = 'FK'
                rel.save()

                rel.id = None
                rel.tipo_campo = 'PK'
                rel.tabela = tabela
                rel.save()

            for campo_id in dict['campos']:
                #campo = Campo.objects.get(id=campo_id)
                rel = Campo_Tabela.objects.get(id=campo_id, tipo_campo='Normal')
                rel.tabela = tabela
                rel.save()


        return {}