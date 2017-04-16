from app.models import Grupo, Grupo_Usuario, Usuario
from classes.util_grupo import *


def run_grupo(request, grupo_id):
    if request.method == 'GET':
        grupo = Grupo.objects.get(id=grupo_id)

        array_usuarios = listar_usuarios_do_grupo(grupo_id)

        grupo.usuarios = array_usuarios

        return {'grupo': grupo}