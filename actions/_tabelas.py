from app.forms import TableForm
from app.models import *

from classes.util_documento import *


def run_tabelas(request):

    usuario_id = request.session['usuario_id']
    documentos = listar_documentos_usuario(usuario_id)

    for documento in documentos:
        documento.tabelas = listar_tabelas_documento(documento.id)

    return {'documentos': documentos}