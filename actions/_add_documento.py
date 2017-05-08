from app.forms import DocumentForm, FieldForm
from app.models import Documento, Tabela, Campo, Campo_Tabela, Grupo

from classes.util_grupo import *
from classes.util import *


def run_add_documento(request):
    id_usuario = request.session['usuario_id']
    formDoc = DocumentForm()
    formCamp = FieldForm()

    if request.method == 'POST':
        array_post = request.POST

        """
            CRIA UM NOVO REGISTRO DE DOCUMENTO
        """
        documento_novo = Documento()
        documento_novo.nome = array_post['nome']
        
        """
            SELECIONA O OBJETO DO GRUPO AO QUAL O DOCUMENTO SERA ATRIBUIDO
        """
        grupo = Grupo.objects.get(id=array_post['grupo'])
        documento_novo.grupo = grupo
        
        documento_novo.save()

        """
            CRIA UMA ESTRUTURA BASE PARA ARMAZENAR OS CAMPOS
        """
        tabela_base = Tabela()
        tabela_base.documento = documento_novo
        tabela_base.nome = 'tabela_base'
        tabela_base.tabela_tipo = 0
        tabela_base.save()

        array_campos = []
        for key, val in array_post.items():
            if 'campo' in key:
                aux = {
                    'nome': val,
                    'pos': key[-2]
                }
                array_campos.append(aux)

        for campo in array_campos:
            temp = Campo()
            temp.nome = underlined(campo['nome'])
            temp.save()

            tb_campo = Campo_Tabela(campo=temp, tabela=tabela_base, tipo_campo='Normal')
            tb_campo.save()


        return {'resultado': True}

    elif request.method == 'GET':
        grupos = listar_grupos_do_usuario(id_usuario, 'normal')

        return {'resultado': True, 'form_documento': formDoc, 'formCamp': formCamp, 'grupos': grupos}

