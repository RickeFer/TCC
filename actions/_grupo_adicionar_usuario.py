from app.models import Grupo_Usuario, Usuario, Grupo


def run_grupo_adicionar_usuario(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)

    if request.method == 'POST':
        array_post = request.POST

        email = array_post['email']

        """
            ENVIA UMA SOLICITACAO PARA PARTICIPAR DO GRUPO
        """
        try:
            usuario = Usuario.objects.get(email=email)
            grupo = Grupo.objects.get(id=grupo_id)

            rel = Grupo_Usuario(grupo=grupo, usuario=usuario, situacao='pendente')
            rel.save()

            return {'resultado': True}

        except:
            return {'resultado': False, 'grupo': grupo}


    elif request.method == 'GET':
        """
        array_temp = Usuario.objects.all()

        array_usuario = []
        for temp in array_temp:
            try:
                rel = Grupo_Usuario.objects.get(grupo=grupo, usuario=temp)
            except:
                array_usuario.append(temp)
        """

        return {'resultado': True, 'grupo': grupo}
    else:

        return {'resultado': False}