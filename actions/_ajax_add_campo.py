from app.models import *

def run_ajax_add_campo(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        campo = Campo()
        campo.nome = nome

        documento = Documento.objects.get(id=request.POST['documento'])
        tabela = documento.tabela_set.get(tabela_tipo=0)

        campo.tabela = tabela

    return {'pag': request.POST['pag'], 'campo': campo}