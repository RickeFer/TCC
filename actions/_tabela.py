from app.models import *
from classes.util_tabela import *
from classes.util import *


def run_tabela(request, tabela_id):

    if request.method == 'POST':
        array_post = request.POST

        dic_campos = {}

        for key, valor in array_post.items():
            if 'tipo' in key:
                temp_id = key.split('_')[1]
                dic_campos[temp_id] = {'tipo': valor}

        for key, valor in array_post.items():
            if 'unsigned' in key and valor == 'on':
                temp_id = key.split('_')[1]
                dic_campos[temp_id]['unsigned'] = True
            if 'zerofill' in key and valor == 'on':
                temp_id = key.split('_')[1]
                dic_campos[temp_id]['zerofill'] = True
            if 'null' in key and valor == 'on':
                temp_id = key.split('_')[1]
                dic_campos[temp_id]['null'] = True
            if 'tamanho' in key:
                temp_id = key.split('_')[1]
                dic_campos[temp_id]['tamanho'] = valor


        for id, propriedades in dic_campos.items():
            campo = Campo.objects.get(id=id)
            campo.unsigned = False
            campo.zerofill = False
            campo.null = False

            for propriedade, valor in propriedades.items():
                if propriedade == 'tipo':
                    campo.tipo_atributo = valor
                if propriedade == 'unsigned':
                    campo.unsigned = True
                if propriedade == 'zerofill':
                    campo.zerofill = True
                if propriedade == 'null':
                    campo.null = True
                if propriedade == 'tamanho':
                    campo.tamanho_itens = valor

            campo.save()


    tabela = Tabela.objects.get(id=tabela_id)
    tabela.campos = listar_campos_tabela(tabela, False)
    tabela.primarias = listar_chaves_tabela(tabela, 'PK')
    tabela.estrangeiras = listar_chaves_tabela(tabela, 'FK')

    array_tipo_campo = get_array_tipos_campo()
    array_tipo_chave = get_array_tipos_chave()

    return {'tabela': tabela, 'tipos_campo': array_tipo_campo, 'tipos_chave': array_tipo_chave}