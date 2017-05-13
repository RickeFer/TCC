from app.models import *


def get_dados(campo_id):
    campo = Campo.objects.get(id=campo_id)

    return campo.dado_exemplo_set.all()