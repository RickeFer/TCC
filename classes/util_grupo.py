from app.models import Grupo_Usuario, Grupo, Usuario


def listar_grupos_do_usuario(id_usuario, situacao='todos'):
    usuario = Usuario.objects.get(id=id_usuario)

    if situacao != 'todos':
        array_temp = Grupo_Usuario.objects.filter(usuario=usuario, situacao=situacao)
    else:
        array_temp = Grupo_Usuario.objects.filter(usuario=usuario)

    array_grupos = []
    for rel in array_temp:
        array_grupos.append(rel.grupo)

    return array_grupos


def listar_usuarios_do_grupo(id_grupo):
    grupo = Grupo.objects.get(id=id_grupo)

    array_temp = Grupo_Usuario.objects.filter(grupo=grupo, situacao='normal')
    array_usuarios = []

    for rel in array_temp:
        array_usuarios.append(rel.usuario)

    return array_usuarios


def listar_solicitacoes(id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)

    array_rel = Grupo_Usuario.objects.filter(usuario=usuario, situacao='pendente')

    return array_rel