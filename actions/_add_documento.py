from app.forms import DocumentForm, FieldForm
from app.models import Documento, Tabela, Campo
import pprint


def run_add_documento(request):
    formDoc = DocumentForm()
    formCamp = FieldForm()

    if request.method == 'POST':
        postDic = request.POST.dict()

        #cria um novo documento
        documento_novo = Documento()
        documento_novo.nome = postDic['nome']
        documento_novo.save()

        #cria uma tabela base com o mesmo nome do documento
        #para armazenar os campos
        tabela_base = Tabela()
        tabela_base.documento = documento_novo
        tabela_base.nome = 'tabela_base'#postDic['name']
        tabela_base.tabela_tipo = 0
        tabela_base.save()

        array_campos = []
        for key, val in postDic.items():
            if 'campo' in key:
                aux = {
                    'nome': val,
                    'pos': key[-2]
                }
                array_campos.append(aux)

        for campo in array_campos:
            temp = Campo()
            temp.tabela = tabela_base
            temp.ordem = campo['pos']
            temp.nome = campo['nome']
            temp.save()


    return {'formDoc': formDoc, 'formCamp': formCamp}