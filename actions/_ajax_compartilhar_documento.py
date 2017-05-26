from classes.util_documento import *

from app.models import *


def run_ajax_compartilhar_documento(request):
    array_post = request.POST

    """
        COMPARTILHAR ESTADO ATUAL DO DOCUMENTO.
    """
    if array_post['modo_compartilhar'] == 2:
        documento = Documento.objects.get(id=array_post['documento_id'])

        tabelas = documento.tabela_set.all()

        rels = {}
        for tabela in tabelas:
            for rel in tabela.campo_tabela_set.all():
                rels[rel.id] = rel

        print(rels)
        print(len(rels))
        return {}
        campos = {}

        for rel in rels:
            campos[rel.id] = rel.campo

        print(campos)

    #get_documento_completo(array_post['documento_id'])




    return {}