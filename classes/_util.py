class Util:
    def get_array_tipos_restricao():
        tupla = (
            ('PK', 'Chave Primária'),
            ('FK', 'Chave Estrangeira'),
            ('Normal', 'Campo Normal')
        )

        return tupla

import random
import string

def gerarHash(tamanho=16):
    aux = string.ascii_lowercase + string.digits

    saida = ''
    for i in range(tamanho):
        saida += random.choice(aux)

    return saida