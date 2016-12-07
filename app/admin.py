from django.contrib import admin
# Register your models here.

from .models import *

admin.site.register(Table)
admin.site.register(Field)
admin.site.register(Document)
