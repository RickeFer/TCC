from app.models import *


def run_ajax_desnormalizar_documento(request):
    array_post = request.POST

    documento = Documento.objects.get(id=array_post['documento_id'])

    tabela_base = documento.tabela_set.get(nome='tabela_base')
    tabelas = documento.tabela_set.all().exclude(nome='tabela_base')
    dict_tabelas = {}

    for tabela in tabelas:
        dict_tabelas[tabela.id] = {'campos': {}, 'rels': [], 'tabela': tabela}
        for rel in tabela.campo_tabela_set.all().exclude(tipo_campo='FK'):
            dict_tabelas[tabela.id]['campos'][rel.campo.id] = rel.campo
            dict_tabelas[tabela.id]['rels'].append(rel)


    for chave, item in dict_tabelas.items():
        for rel in item['rels']:
            rel.tipo_campo = 'Normal'
            rel.campo = item['campos'][rel.campo.id]
            rel.tabela = tabela_base
            rel.save()

    for tabela in tabelas:
        tabela.delete()

    return {'resultado': True}