from app.models import *
from classes.util_grupo import *
from classes.util_tabela import *


def listar_documentos_usuario(id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)

    array_grupo = listar_grupos_do_usuario(id_usuario, 'normal')

    print(array_grupo)
    array_documento = []
    for grupo in array_grupo:
        array_temp = Documento.objects.filter(grupo=grupo)
        for temp in array_temp:
            array_documento.append(temp)

    return array_documento


def get_campo_documento(id_documento, nome=False, id=False):
    documento = Documento.objects.get(id=id_documento)

    tabelas = documento.tabela_set.all()

    for tabela in tabelas:
        array_campo = listar_campos_tabela(tabela)
        for campo in array_campo:
            if nome:
                if campo.nome == nome:
                    return campo
            elif id:
                if campo.id == id:
                    return campo

    return None


def get_chave_documento(id_documento, nome=False, id=False, restricao='PK'):
    documento = Documento.objects.get(id=id_documento)

    tabelas = documento.tabela_set.all()

    for tabela in tabelas:
        array_campo = listar_chaves_tabela(tabela, restricao)
        for campo in array_campo:
            if nome:
                if campo.nome == nome:
                    return campo
            elif id:
                if campo.id == id:
                    return campo

    return None