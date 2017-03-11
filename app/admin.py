from django.contrib import admin
# Register your models here.

from .models import *

admin.site.register(Tabela)
admin.site.register(Campo)
admin.site.register(Documento)
