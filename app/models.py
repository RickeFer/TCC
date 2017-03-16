from django.db import models

from classes._util import Util

array_tipo_restricao = Util.get_array_tipos_restricao()

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

    def __str__(self):
        return self.nome

    def nome_sublinhado(self):
        aux = self.nome.split()
        ret = ''
        for c in aux:
            ret += c+'_'

        return ret[:-1]


class Campo(models.Model):
    tabela = models.ForeignKey(Tabela, default=None)
    nome = models.CharField(max_length=20)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    ordem = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nome

    def name_underlined(self):
        aux = self.nome.split()
        ret = ''
        for c in aux:
            ret += c+'_'

        return ret[:-1]


class Dependencia(models.Model):
    campo = models.ForeignKey(Campo, related_name="campo")
    chave = models.ForeignKey(Campo, related_name="dependente")

    def __str__(self):
        return self.campo.nome+' '+self.chave.nome


class Restricao(models.Model):
    campo = models.ForeignKey(Campo)
    tipo = models.CharField(max_length=20, choices=array_tipo_restricao)

