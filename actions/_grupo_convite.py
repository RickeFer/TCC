from app.models import Grupo_Usuario, Usuario, Grupo


def run_grupo_convite(request):
    if request.method == 'POST':
        array_post = request.POST

        id_usuario = request.session.get('usuario_id')

        usuario = Usuario.objects.get(id=id_usuario)
        grupo = Grupo.objects.get(id=array_post['grupo'])

        grupo_rel = Grupo_Usuario.objects.get(usuario=usuario, grupo=grupo)

        if array_post.get('aceitar', False):
            grupo_rel.situacao = 'normal'
            grupo_rel.save()

            return {'resultado': True}

        if array_post.get('rejeitar', False):
            grupo_rel.situacao = 'rejeitada'
            grupo_rel.save()

            return {'resultado': True}