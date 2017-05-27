from app.models import *

from classes.util_documento import *


def run_forma_normal_3(request, documento_id):

    if request.method == 'GET':
        documento = get_documento_completo(documento_id)

        return {'fn':2, 'documento':documento}

    elif request.method == 'POST':
        array_post = request.POST

        documento = Documento.objects.get(id=documento_id)

        dicionario_dependencia, array_novas_tabelas = {}, []


        """
            MONTA UM DICIONARIO COM AS DEPENDENCIAS
            E CRIA UMA TABELA PARA CADA CHAVE NO DICIONARIO
        """
        for item in array_post:
            if 'dependencia' in item:
                nome_dependente = item.split('_dependencia')[0]
                nome_chave = array_post[item]

                if dicionario_dependencia.get(nome_chave, None):
                    dicionario_dependencia[nome_chave].append(nome_dependente)
                else:
                    dicionario_dependencia[nome_chave] = [nome_dependente]

                    hash = gerar_hash(16)
                    nova_tabela = Tabela(documento=documento, nome=hash, forma_normal=3, renomear=True)
                    nova_tabela.save()
                    array_novas_tabelas.append(nova_tabela)

        """
            PASSA OS CAMPOS DEPENDENTES PARA AS NOVAS TABELAS
        """
        for key, array_campos in dicionario_dependencia.items():
            campo = get_campo_documento(documento_id, nome=key)
            rel = campo.campo_tabela_set.get(tipo_campo='Normal')
            rel.tipo_campo = 'FK'
            rel.save()

            tabela = array_novas_tabelas.pop()

            # duplica a fk para ser pk na nova tabela
            rel.id = None
            rel.tipo_campo = 'PK'
            rel.tabela = tabela
            rel.save()

            for nome_campo in array_campos:
                campo = get_campo_documento(documento_id, nome=nome_campo)
                rel = campo.campo_tabela_set.get(tipo_campo='Normal')
                rel.tabela = tabela
                rel.save()

        """
            PASSA AS TABELAS PARA A 3FN
        """
        tabelas = documento.tabela_set.filter(tabela_tipo=1)
        for tabela in tabelas:
            tabela.forma_normal = 3
            tabela.save()

        return {}