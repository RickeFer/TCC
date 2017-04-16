from classes.util_documento import *


def run_documentos(request):
    id_usuario = request.session['usuario_id']

    documentos = listar_documentos_usuario(id_usuario)

    return {'documentos': documentos}