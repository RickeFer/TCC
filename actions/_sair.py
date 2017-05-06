from classes.util import *


def run_sair(request):
    del request.session['sessao_hash']

    return {}