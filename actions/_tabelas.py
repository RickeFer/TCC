from app.forms import TableForm
from app.models import *


def run_tabelas():
    form = TableForm()
    tabelas = Tabela.objects.all().exclude(tabela_tipo=0)
    return {'tabelas': tabelas, 'form': form}