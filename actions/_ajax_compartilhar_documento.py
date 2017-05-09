from classes.util_documento import *


def run_ajax_compartilhar_documento(request):
    array_post = request.POST

    documento = get_documento_completo(array_post['documento_id'])


    return {}