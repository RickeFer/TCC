class Util:
    def get_array_tipos_restricao():
        tupla = (
            ('PK', 'Chave Primária'),
            ('FK', 'Chave Estrangeira'),
            ('Normal', 'Campo Normal')
        )

        return tupla


def get_array_campos_sem_tabela(tabela_base):


    return campos_sem_tabela