from app.models import *


def run_ajax_dados_exemplo(request):

    if request.method == 'POST':
        array_post = request.POST
        id = 0

        if int(array_post['dado_id']) == 0:
            # inserir
            try:
                campo = Campo.objects.get(id=array_post['campo_id'])
                dado_exemplo = Dado_Exemplo(texto=array_post['dado'], campo=campo)
                dado_exemplo.save()
                id = dado_exemplo.id
                res = True
            except:
                res = False

        else:
            #alterar
            if array_post.get('acao', '') == 'remover':
                try:
                    dado_exemplo = Dado_Exemplo.objects.get(id=array_post['dado_id'])
                    dado_exemplo.delete()
                    res = True
                except:
                    res = False
            elif array_post.get('acao', '') == 'adicionar':
                try:
                    dado_exemplo = Dado_Exemplo.objects.get(id=array_post['dado_id'])
                    dado_exemplo.texto = array_post['dado']
                    dado_exemplo.save()
                    res = True
                    id = dado_exemplo.id
                except:
                    res = False


    return {'resultado':res, 'dado_id':id}