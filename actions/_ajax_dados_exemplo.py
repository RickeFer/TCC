from app.models import *


def run_ajax_dados_exemplo(request):

    if request.method == 'POST':
        array_post = request.POST

        if int(array_post['dado_id']) != 0:
            #alterar
            if array_post['dado']=='':
                dado_exemplo = Dado_Exemplo.objects.get(id=array_post['dado_id'])
                dado_exemplo.delete()
            else:
                try:
                    dado_exemplo = Dado_Exemplo.objects.get(id=array_post['dado_id'])
                    dado_exemplo.texto = array_post['dado']
                    dado_exemplo.save()
                    res = True
                except:
                    res = False

        else:
            #inserir
            try:
                campo = Campo.objects.get(id=array_post['campo_id'])
                dado_exemplo = Dado_Exemplo(texto=array_post['dado'], campo=campo)
                dado_exemplo.save()
                res = True
            except:
                res = False


    return {'resultado':res}