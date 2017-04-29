from classes.util_documento import *


def run_diagrama_documento(request, documento_id):
    documento = get_documento_completo(documento_id)

    return {'documento': documento}