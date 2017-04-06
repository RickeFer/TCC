from django.db import models


array_tipo_restricao = tupla = (
        ('PK', 'Chave Primária'),
        ('FK', 'Chave Estrangeira'),
        ('Normal', 'Campo Normal')
    )


class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=20)
    senha = models.CharField(max_length=64)
    ultima_hash = models.CharField(max_length=64)

    def __str__(self):
        return self.nome


class Documento(models.Model):
    nome = models.CharField(max_length=20)
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

    def nome_sublinhado(self):
        aux = self.nome.split()
        ret = ''
        for c in aux:
            ret += c+'_'

        return ret[:-1]


class Campo(models.Model):
    #tabela = models.ForeignKey(Tabela, default=None)
    nome = models.CharField(max_length=20)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    ordem = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nome


class Dependencia(models.Model):
    campo = models.ForeignKey(Campo, related_name="campo")
    chave = models.ForeignKey(Campo, related_name="dependente")

    def __str__(self):
        return self.campo.nome+' '+self.chave.nome


class Campo_Tabela(models.Model):
    campo = models.ForeignKey(Campo)
    tabela = models.ForeignKey(Tabela)
    tipo_campo = models.CharField(max_length=20, choices=array_tipo_restricao)

    def __str__(self):
        return self.campo.nome

