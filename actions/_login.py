from app.models import Usuario
import hashlib
from django.utils import timezone

from classes.util import *

def run_login(request):
    if request.method == 'POST':
        array_post = request.POST

        email = array_post['email']
        senha = array_post['senha']
        hash_senha = hashlib.sha224(senha.encode('utf8'))
        senha = hash_senha.hexdigest()

        #verifica se o usuario existe
        try:
            usuario = Usuario.objects.get(email=email, senha=senha)

            hash_monstra = gerar_hash_session(usuario.nome, usuario.senha)
            usuario.ultima_hash = hash_monstra
            usuario.ultimo_login = timezone.now()
            usuario.save()

            return {'resultado': True, 'sessao_hash': usuario.ultima_hash, 'usuario_id': usuario.id}
        except:
            return {'resultado': False, 'erro': 'deu ruim'}
