from app.models import *
from app.forms import TableForm


def run_normalizar(documento_id):
    documento = Documento.objects.get(id=documento_id)

    """
    tabela = Table.objects.get(id=table_id)
    campos = tabela.campo_set.order_by('ordem')

    # separa linhas de 8 campos em um dicionario
    if len(campos) > 8:
        dicCampos = {};
        aux = [];
        cont = 0
        for c in campos:
            aux.append(c)
            if c.order % 8 == 0:
                dicCampos[cont] = aux
                aux = []
                cont += 1
        if len(aux):
            dicCampos[cont] = aux
            # campos = dicCampos
    else:
        dicCampos = {campos}
        # campos = dicCampos

    tabelas = Table.objects.all()
    context = {'tabela': tabela, 'tabelas': tabelas, 'dicCampos': dicCampos, 'form': TableForm()}
    """
    return {'form': TableForm(), 'documento': documento}