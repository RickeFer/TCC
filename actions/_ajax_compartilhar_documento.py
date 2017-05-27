from classes.util_documento import *

from app.models import *


def run_ajax_compartilhar_documento(request):
    array_post = request.POST

    grupo_novo = Grupo.objects.get(id=array_post['grupo_id'])

    """
        COMPARTILHAR ESTADO ATUAL DO DOCUMENTO
    """

    if int(array_post['modo_compartilhar']) == 2:
        documento = Documento.objects.get(id=array_post['documento_id'])

        tabelas = documento.tabela_set.all()
        dict_tabelas = {}

        for tabela in tabelas:
            dict_tabelas[tabela.id] = {'campos':{}, 'rels':[], 'tabela':tabela}
            for rel in tabela.campo_tabela_set.all():
                dict_tabelas[tabela.id]['campos'][rel.campo.id] = rel.campo
                dict_tabelas[tabela.id]['rels'].append(rel)

        documento.id = None
        documento.grupo = grupo_novo
        documento.save()

        dict_campos_atual = {}
        for chave, item in dict_tabelas.items():
            tabela_temp = item['tabela']
            tabela_temp.id = None
            tabela_temp.documento = documento
            tabela_temp.save()

            for rel in item['rels']:

                if dict_campos_atual.get(rel.campo.id, False):
                    rel.id = None
                    rel.campo = dict_campos_atual[rel.campo.id]
                    rel.tabela = tabela_temp
                    rel.save()

                else:
                    campo_aux = item['campos'][rel.campo.id]
                    id_antigo = campo_aux.id

                    campo_aux.id = None
                    campo_aux.save()

                    dict_campos_atual[id_antigo] = campo_aux

                    rel.id = None
                    rel.campo = campo_aux
                    rel.tabela = tabela_temp
                    rel.save()

        return {'resultado':True}

    #get_documento_completo(array_post['documento_id'])




    return {'post':array_post}