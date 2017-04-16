from app.models import *


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