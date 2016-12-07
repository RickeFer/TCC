from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    document = models.ForeignKey(Document)
    name = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    normal_form = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def name_underlined(self):
        aux = self.name.split()
        ret = ''
        for c in aux:
            ret += c+'_'

        return ret[:-1]


class Field(models.Model):
    table = models.ForeignKey(Table, default=None)
    name = models.CharField(max_length=20)
    primary = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    def name_underlined(self):
        aux = self.name.split()
        ret = ''
        for c in aux:
            ret += c+'_'

        return ret[:-1]
