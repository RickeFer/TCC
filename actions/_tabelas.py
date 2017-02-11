from app.forms import TableForm
from app.models import *


def runTabelas():
    form = TableForm()
    tabelas = Table.objects.all().exclude(type_table=0)
    return {'tabelas': tabelas, 'form': form}