from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import random
import string
import hashlib

from app.models import Usuario


def get_array_tipos_restricao():
    tupla = (
        ('PK', 'Chave Primária'),
        ('FK', 'Chave Estrangeira'),
        ('Normal', 'Campo Normal')
    )

    return tupla


def gerarHash(tamanho=16):
    aux = string.ascii_lowercase + string.digits

    saida = ''
    for i in range(tamanho):
        saida += random.choice(aux)

    return saida


def gerar_hash_session(nome, senha):
    hash_nome = hashlib.sha224(nome.encode('utf8'))
    hash_senha = hashlib.sha224(senha.encode('utf8'))

    temp_nome = hash_nome.hexdigest()
    temp_senha = hash_senha.hexdigest()

    hash_monstrao = hashlib.sha224(temp_nome.encode('utf8')+temp_senha.encode('utf8'))

    return hash_monstrao.hexdigest()


def verificar_sessao(request):
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])

        hash2 = gerar_hash_session(usuario.nome, usuario.senha)

        if request.session['sessao_hash']==hash2:
            return True
        else:
            redirecionar_login()
    except:
        redirecionar_login()


def redirecionar_login():
    return HttpResponseRedirect(reverse('users:login'))


def get_usuario(id):
    usuario = Usuario.objects.get(id=id)

    return usuario