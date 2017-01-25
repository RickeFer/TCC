from app.models import *
from app.forms import TableForm


def run_normalizar_documento(documento_id):
    documento = Document.objects.get(id = documento_id)

    #pega os campos sem tabela
    tabela_base = documento.table_set.get(name=documento.name)
    campos_sem_tabela = tabela_base.field_set.order_by('order')

    arrayTabelas = []
    #pega outras tabela e seus campos
    tabelas = documento.table_set.exclude(name=documento.name)
    for tabela in tabelas:
        campos = tabela.field_set.order_by('order')
        aux = {'tabela': tabela, 'campos': campos}
        arrayTabelas.append(aux)

    print(arrayTabelas)

    tabela_form = TableForm()

    context = {'documento': documento, 'sem_tabela': campos_sem_tabela, 'arrayTabelas': arrayTabelas, 'tabela_form': tabela_form}
    return context