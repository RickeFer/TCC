from classes.util_grupo import *


def run_grupos(request):

    id_usuario = request.session.get('usuario_id')

    array_grupo = listar_grupos_do_usuario(id_usuario, 'normal')

    return {'grupos': array_grupo}