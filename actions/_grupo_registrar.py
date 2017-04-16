from app.models import Grupo, Usuario, Grupo_Usuario

def run_grupo_registrar(request):
    if request.method == 'POST':
        array_post = request.POST

        try:
            usuario = Usuario.objects.get(id=array_post['id_usuario'])

            grupo = Grupo(nome=array_post['nome'])
            grupo.save()

            grupo_usuario = Grupo_Usuario(usuario=usuario, grupo=grupo)
            grupo_usuario.save()

            return {'resultado': True}
        except:
            return {'resultado': False}

    elif request.method == 'GET':

        return {'resultado': True}
    else:

        return {'resultado': False}