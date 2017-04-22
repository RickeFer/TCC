from app.models import *

from classes.util import *


def get_tabela_do_documento(id_documento, nome=False, id=False):
    documento = Documento.objects.get(id=id_documento)

    try:
        if nome:
            tabela = documento.tabela_set.get(nome=nome)
        elif id:
            tabela = documento.tabela_set.get(id=id)

        return tabela
    except:

        return None

    return None


def listar_campos_tabela(tabela, chaves=True):
    if chaves:
        rel_temp = tabela.campo_tabela_set.all()
    else:
        rel_temp = tabela.campo_tabela_set.filter(tipo_campo='Normal')

    array_campo = []
    for rel in rel_temp:
        array_campo.append(rel.campo)

    return array_campo


def listar_chaves_tabela(tabela, restricao='PK'):
    if restricao == 'PK':
        rel_temp = tabela.campo_tabela_set.filter(tipo_campo='PK')
    else:
        rel_temp = tabela.campo_tabela_set.filter(tipo_campo='FK')

    array_campo = []
    for rel in rel_temp:
        array_campo.append(rel.campo)

    return array_campo


def gerar_script_create(tabela):
    script = 'CREATE TABLE '+tabela.nome.lower()+'\n('

    """
        CHAVES
    """
    for primaria in tabela.primarias:
        script += '\n\t'+primaria.nome.lower()
        script += ' '+primaria.tipo_atributo+' NOT NULL,'
    for primaria in tabela.estrangeiras:
        script += '\n\t'+primaria.nome.lower()
        script += ' '+primaria.tipo_atributo+' NOT NULL,'

    """
        CAMPOS
    """
    for campo in tabela.campos:
        script += '\n\t'+campo.nome.lower()
        script += ' '+campo.tipo_atributo

        if get_tipo_propriedade(campo.tipo_atributo) == 'TEXT':
            script += '('+str(campo.tamanho_itens)+')'
            script += ' NULL' if campo.null else ' NOT NULL'

        if get_tipo_propriedade(campo.tipo_atributo) == 'INT':
            script += ' NULL' if campo.null else ' NOT NULL'
            script += ' UNSIGNED' if campo.unsigned else ''
            script += ' ZEROFILL' if campo.zerofill else ''

        if get_tipo_propriedade(campo.tipo_atributo) == 'DATE':
            script += ' NULL' if campo.null else ' NOT NULL'

        if get_tipo_propriedade(campo.tipo_atributo) == 'FLOAT':
            script += '(' + str(campo.tamanho_itens) + ')'
            script += ' NULL' if campo.null else ' NOT NULL'
            script += ' UNSIGNED' if campo.unsigned else ''
            script += ' ZEROFILL' if campo.zerofill else ''

        script += ','

    script = script[:-1]+'\n);\n\n';

    return script


def gerar_script_alter_primaria(tabela):
    script = 'ALTER TABLE '+tabela.nome.lower()
    script += '\nADD CONSTRAINT PK_'+tabela.nome.lower()
    script += ' PRIMARY KEY ('

    for chave in tabela.primarias:
        script += chave.nome.lower()+','
    for chave in tabela.estrangeiras:
        script += chave.nome.lower()+','

    script  = script[:-1]+');\n\n'

    return script

def gerar_script_alter_estrangeira(tabela):
    script = 'ALTER TABLE ' + tabela.nome.lower()

    if tabela.estrangeiras:
        for chave in tabela.estrangeiras:
            rel_temp = Campo_Tabela.objects.get(campo=chave, tipo_campo='PK')

            script += '\nADD CONSTRAINT FK_'+rel_temp.tabela.nome.lower().title()
            script += tabela.nome.lower().title()
            script += '\nFOREIGN KEY ('+chave.nome.lower()+')'
            script += ' REFERENCES '+rel_temp.tabela.nome.lower()
            script += '('+chave.nome.lower()+');'
            script += '\n\n';

        return script
    else:
        return ''