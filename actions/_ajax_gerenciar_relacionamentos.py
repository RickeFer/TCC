from app.models import *


def run_ajax_gerenciar_relacionamentos(request):
    array_post = request.POST

    try:
        campo_fonte = Campo.objects.get(id=array_post['fonte'])
        rels_fonte = campo_fonte.campo_tabela_set.all()

        campo_ref = Campo.objects.get(id=array_post['referencia'])

        for rel in rels_fonte:
            rel.campo = campo_ref
            rel.tipo_campo = 'FK'
            rel.save()

        campo_fonte.delete()

        return {'resultado': True}
    except:

        return {'resultado': False}