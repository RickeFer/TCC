from app.forms import DocumentForm, FieldForm
from app.models import Documento, Tabela, Campo, Campo_Tabela, Grupo
from classes.util_grupo import *


def run_add_documento(request):
    id_usuario = request.session['usuario_id']
    formDoc = DocumentForm()
    formCamp = FieldForm()

    if request.method == 'POST':
        array_post = request.POST

        #cria um novo documento
        documento_novo = Documento()
        documento_novo.nome = array_post['nome']
        
        #seleciona o grupo do documento
        grupo = Grupo.objects.get(id=array_post['grupo'])
        documento_novo.grupo = grupo
        
        documento_novo.save()

        #cria uma tabela base com o mesmo nome do documento
        #para armazenar os campos
        tabela_base = Tabela()
        tabela_base.documento = documento_novo
        tabela_base.nome = 'tabela_base'#array_post['name']
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
            #temp.tabela = tabela_base
            temp.ordem = campo['pos']
            temp.nome = campo['nome']
            temp.save()

            tb_campo = Campo_Tabela(campo=temp, tabela=tabela_base, tipo_campo='Normal')
            tb_campo.save()


        return {'resultado': True, 'formDoc': formDoc, 'formCamp': formCamp}

    elif request.method == 'GET':
        grupos = listar_grupos_do_usuario(id_usuario, 'normal')

        return {'resultado': True, 'formDoc': formDoc, 'formCamp': formCamp, 'grupos': grupos}

