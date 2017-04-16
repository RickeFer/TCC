from classes.util_grupo import *


def run_index(request):
    id_usuario = request.session['usuario_id']

    """
        LISTA AS SOLICITACOES DE GRUPO
    """

    solicitacoes = listar_solicitacoes(id_usuario)

    return {'solicitacoes': solicitacoes}