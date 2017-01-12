from app.forms import TableForm
from app.models import *


def runTabelas():
    form = TableForm()
    tabelas = Table.objects.all().exclude(normal_form=-1)
    return {'tabelas': tabelas, 'form': form}