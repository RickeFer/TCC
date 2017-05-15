from app.models import *

from classes.util_documento import *
from classes.util_campo import *
from classes.util import *


def run_forma_normal_1(request, documento_id):
    documento = Documento.objects.get(id=documento_id)
    documento.uni, documento.multi = [], []


    if request.method == 'GET':
        campos_temp = listar_campos_sem_tabela(documento_id)

        for campo in campos_temp:
            campo.dados = get_dados(campo.id)

            if len(campo.dados)>1:
                documento.multi.append(campo)
            else:
                documento.uni.append(campo)

        hashe = gerar_hash()

        return {'fn': 0, 'documento':documento, 'hashe':hashe}

    elif request.method == 'POST':
        array_post = request.POST

        """
            CRIA AS NOVAS TABELAS
        """
        tabela_uni = Tabela(nome=underlined(array_post['tabela_uni']), forma_normal=1, tabela_tipo=1, documento=documento, renomear=False)
        tabela_multi = Tabela(nome=underlined(array_post['tabela_multi']), forma_normal=1, tabela_tipo=1, documento=documento, renomear=False)
        if array_post['hashe'] == array_post['tabela_multi']:
            tabela_multi.renomear = True


        """
            SEPARA OS CAMPOS COM DADOS REPETITIVOS E NAO REPETITIVOS
            EM DICIONARIOS DIFERENTES
        """
        dict_uni, dict_multi = {'chaves':[], 'campos':[]}, {'chaves':[], 'campos':[]}

        for chave, valor in array_post.items():
            if 'uni[' in chave:
                campo = Campo.objects.get(id=valor)
                temp = Campo_Tabela.objects.get(campo=campo)

                if int(array_post.get('primaria['+valor+']', 0)):
                    temp.tipo_campo = 'PK'
                    dict_uni['chaves'].append(temp)
                else:
                    dict_uni['campos'].append(temp)

            if 'multi[' in chave:
                campo = Campo.objects.get(id=valor)
                temp = Campo_Tabela.objects.get(campo=campo)

                if int(array_post.get('primaria[' + valor + ']', 0)):
                    temp.tipo_campo = 'PK'
                    dict_multi['chaves'].append(temp)
                else:
                    dict_multi['campos'].append(temp)


        """
            DISTRIBUI OS CAMPOS EM SUAS TABELAS
        """
        tabela_multi.save()
        for campo in dict_multi['campos']+dict_multi['chaves']:
            campo.tabela = tabela_multi
            campo.save()

        tabela_uni.save()
        for campo in dict_uni['campos']+dict_uni['chaves']:
            campo.tabela = tabela_uni
            campo.save()

            if campo.tipo_campo == 'PK':
                campo.id = Nome
                campo.tipo_campo = 'FK'
                campo.tabela = tabela_multi
                campo.save()
                dict_multi['chaves'].append(0)


        """
            DEFINE A FORMA NORMAL DA TABELA DE ACORDO
            COM A QUANTIDADE DE CHAVES
        """
        if len(dict_multi['chaves']) > 1:
            tabela_multi.forma_normal = 1
        else:
            tabela_multi.forma_normal = 2

        if len(dict_uni['chaves']) > 1:
            tabela_uni.forma_normal = 1
        else:
            tabela_uni.forma_normal = 2

        tabela_uni.save()
        tabela_multi.save()


        return {}