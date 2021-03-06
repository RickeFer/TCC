from django.db import models


array_tipo_restricao = (
        ('PK', 'Chave Primária'),
        ('FK', 'Chave Estrangeira'),
        ('Normal', 'Campo Normal')
    )
array_situacao = (
    ('OK', 'Membro'),
    ('Pendente', 'Pendente')
)


class Grupo(models.Model):
    nome = models.CharField(max_length=50)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=64)
    sessao_hash = models.CharField(max_length=64, null=True)
    ultimo_login = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome


class Grupo_Usuario(models.Model):
    usuario = models.ForeignKey(Usuario)
    grupo = models.ForeignKey(Grupo)
    situacao = models.CharField(max_length=10, choices=array_situacao, default='pendente')

    def __str__(self):
        return self.usuario.nome + ' - ' + self.grupo.nome


class Documento(models.Model):
    nome = models.CharField(max_length=20)
    grupo = models.ForeignKey(Grupo)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Tabela(models.Model):
    documento = models.ForeignKey(Documento)
    nome = models.CharField(max_length=20)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    forma_normal = models.PositiveSmallIntegerField(default=0)
    tabela_tipo = models.PositiveSmallIntegerField(default=1)
    renomear = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Campo(models.Model):
    #tabela = models.ForeignKey(Tabela, default=None)
    nome = models.CharField(max_length=20)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    tipo_atributo = models.CharField(max_length=20, default='INT')
    tamanho_itens = models.CharField(max_length=10, blank=True, null=True)
    unsigned = models.BooleanField(default=False)
    null = models.BooleanField(default=False)
    zerofill = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Campo_Tabela(models.Model):
    campo = models.ForeignKey(Campo)
    tabela = models.ForeignKey(Tabela)
    tipo_campo = models.CharField(max_length=20, choices=array_tipo_restricao)

    def __str__(self):
        return self.campo.nome


class Dado_Exemplo(models.Model):
    campo = models.ForeignKey(Campo)
    texto = models.CharField(max_length=25)

    def __str__(self):
        return self.campo.nome + ' - ' + self.texto

