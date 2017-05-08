from app.models import *
from app.forms import TableForm


def run_normalizar(documento_id):
    documento = Documento.objects.get(id=documento_id)


    return {'form': TableForm(), 'documento': documento}