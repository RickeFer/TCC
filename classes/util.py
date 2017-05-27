from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
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


def gerar_hash(tamanho=16):
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


def get_array_tipos_campo():
    array = {
        'Numérico': [
            'BIT',
            'TINYINT',
            'BOOL',
            'SMALLINT',
            'MEDIUMINT',
            'INT',
            'BIGINT',
            'DECIMAL',
            'FLOAT',
            'DOUBLE'
        ],
        'Texto': [
            'CHAR',
            'VARCHAR',
            'BINARY',
            'TINYBLOB',
            'TINYTEXT',
            'BLOB',
            'TEXT',
            'MEDIUMBLOB',
            'MEDIUMTEXT',
            'LONGBLOB',
            'LONGTEXT',
            'ENUM',
            'SET'
        ],
        'Data e Hora': [
            'DATE',
            'DATETIME',
            'TIMESTAMP',
            'TIME',
            'YEAR'
        ]
    }

    return array

def get_array_tipos_chave():
    array = {
        'Inteiro': [
            'BIT',
            'TINYINT',
            'BOOL',
            'SMALLINT',
            'MEDIUMINT',
            'INT',
            'BIGINT',
        ]
    }

    return array


def get_tipo_propriedade(tipo):
    if tipo in ['BIT', 'TINYINT', 'BOOL', 'SMALLINT', 'MEDIUMINT', 'INT', 'BIGINT']:
        return 'INT'

    if tipo in ['DECIMAL', 'FLOAT', 'DOUBLE']:
        return 'FLOAT'

    if tipo in ['DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR']:
        return 'DATE'

    if tipo in ['CHAR', 'VARCHAR', 'BINARY', 'TINYBLOB', 'TINYTEXT', 'BLOB', 'TEXT', 'MEDIUMBLOB', 'MEDIUMTEXT', 'LONGBLOB', 'LONGTEXT', 'ENUM', 'SET']:
        return 'TEXT'


def underlined(entr):
    saida = entr.replace(' ', '_')

    return saida


def array_2_str(array):
    saida = ''

    for item in array:
        saida += str(item)+'_'

    return saida[0:-1]