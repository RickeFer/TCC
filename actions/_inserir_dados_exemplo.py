from app.models import *
from classes.util_documento import *
from classes.util_tabela import *
from classes.util_campo import *


def run_inserir_dados_exemplo(request, documento_id):

    if request.method == 'GET':
        documento = Documento.objects.get(id=documento_id)
        documento.nome = documento.nome.title()

        documento.campos = listar_campos_sem_tabela(documento_id)

        for campo in documento.campos:
            campo.dados = get_dados(campo.id)


        context = {'documento':documento}

    return context