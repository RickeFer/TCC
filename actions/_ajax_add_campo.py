from app.models import *

def run_ajax_add_campo(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        campo = Field()
        campo.name = nome

        documento = Document.objects.get(id=request.POST['documento'])
        tabela = documento.table_set.get(type_table=0)

        campo.table = tabela

    return {'pag': request.POST['pag'], 'campo': campo}