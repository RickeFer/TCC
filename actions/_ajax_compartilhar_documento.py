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

        try:
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

                        try:
                            dados = Dado_Exemplo.objects.filter(campo=campo_aux)
                        except:
                            dados = None

                        campo_aux.id = None
                        campo_aux.save()

                        if dados:
                            for dado in dados:
                                dado.id = None
                                dado.campo = campo_aux
                                dado.save()


                        dict_campos_atual[id_antigo] = campo_aux

                        rel.id = None
                        rel.campo = campo_aux
                        rel.tabela = tabela_temp
                        rel.save()

            return {'resultado':True}
        except:

            return {'resultado': False}

        """
            COMPARTILHAR DOCUMENTO DESNORMALIZADO
        """
    elif int(array_post['modo_compartilhar']) == 1:
        documento = Documento.objects.get(id=array_post['documento_id'])

        tabela_base = documento.tabela_set.get(nome='tabela_base')
        tabelas = documento.tabela_set.all().exclude(nome='tabela_base')
        dict_tabelas = {}

        for tabela in tabelas:
            dict_tabelas[tabela.id] = {'campos': {}, 'rels': [], 'tabela': tabela}
            for rel in tabela.campo_tabela_set.all().exclude(tipo_campo='FK'):
                dict_tabelas[tabela.id]['campos'][rel.campo.id] = rel.campo
                dict_tabelas[tabela.id]['rels'].append(rel)

        try:
            documento.id = None
            documento.grupo = grupo_novo
            documento.save()

            tabela_base.id = None
            tabela_base.documento = documento
            tabela_base.save()

            dict_campos_atual = {}
            for chave, item in dict_tabelas.items():
                for rel in item['rels']:

                    if dict_campos_atual.get(rel.campo.id, False):
                        rel.id = None
                        rel.campo = dict_campos_atual[rel.campo.id]
                        rel.tabela = tabela_base
                        rel.save()

                    else:
                        campo_aux = item['campos'][rel.campo.id]
                        id_antigo = campo_aux.id

                        try:
                            dados = Dado_Exemplo.objects.filter(campo=campo_aux)
                        except:
                            dados = None

                        campo_aux.id = None
                        campo_aux.save()

                        if dados:
                            for dado in dados:
                                dado.id = None
                                dado.campo = campo_aux
                                dado.save()

                        dict_campos_atual[id_antigo] = campo_aux

                        rel.id = None
                        rel.campo = campo_aux
                        rel.tabela = tabela_base
                        rel.save()

            return {'resultado': True}
        except:

            return {'resultado': False}