from app.forms import DocumentForm, FieldForm
from app.models import Document, Table, Field
import pprint


def run_add_documento(request):

    formDoc = DocumentForm()
    formCamp = FieldForm()
    if request.method == 'POST':
        postDic = request.POST.dict()

        #cria um novo documento
        documento_novo = Document()
        documento_novo.name = postDic['name']
        documento_novo.save()

        #cria uma tabela base com o mesmo nome do documento
        #para armazenar os campos
        tabela_base = Table()
        tabela_base.document = documento_novo
        tabela_base.name = postDic['name']
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
            temp = Field()
            temp.table = tabela_base
            temp.order = campo['pos']
            temp.name = campo['nome']
            temp.save()


    return {'formDoc': formDoc, 'formCamp': formCamp}