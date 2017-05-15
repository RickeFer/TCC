from app.models import *
from app.forms import TableForm

from classes.util import gerar_hash
from classes.util_tabela import *
from classes.util_documento import *

from actions._forma_normal_1 import run_forma_normal_1
from actions._forma_normal_2 import run_forma_normal_2
from actions._forma_normal_3 import run_forma_normal_3


def run_normalizar_documento(request, documento_id):

    if request.method == 'GET':
        documento = Documento.objects.get(id=documento_id)

        tabelas_renomear = listar_tabelas_renomear(documento_id)
        print(tabelas_renomear)
        if len(tabelas_renomear):
            documento.tabelas = tabelas_renomear

            return {'renomear_tabelas': True, 'documento':documento}

        #pega outras tabela e seus campos
        tabelas = documento.tabela_set.exclude(nome='tabela_base')
        nomes_tabelas, fn, arrayTabelas = '', 3, []

        if len(tabelas):
            for tabela in tabelas:
                if tabela.forma_normal < fn:
                    fn = tabela.forma_normal
        else:
            fn = 0


        if fn == 0:
            return run_forma_normal_1(request, documento_id)

        elif fn == 1:#FN2
            return run_forma_normal_2(request, documento_id)

        elif fn == 2:
            return run_forma_normal_3(request, documento_id)

        elif fn == 3:
            context = {'documento': documento}

        return context


    elif request.method == 'POST':
        aux = request.POST

        if aux['forma_normal'] == '1':

            return run_forma_normal_1(request, documento_id)

        elif aux['forma_normal'] == '2':

            return run_forma_normal_2(request, documento_id)
			
        elif aux['forma_normal'] == '3':

            return run_forma_normal_3(request, documento_id)