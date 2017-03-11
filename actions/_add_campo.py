from app.forms import FieldForm
from app.models import *


def runAdd_campo(request, table_id):
    tabela = Tabela.objects.get(id=table_id)

    if request.method != 'POST':
        form = FieldForm()
    else:
        form = FieldForm(data=request.POST)
        if form.is_valid():
            novo_campo = form.save(commit=False)
            # relaciona tabela
            novo_campo.table = tabela
            ult_campo = tabela.field_set.order_by('order')

            if len(ult_campo):
                ult_campo = ult_campo[len(ult_campo) - 1].order
            else:
                ult_campo = -1

            novo_campo.order = ult_campo + 1
            novo_campo.save()
            #return HttpResponseRedirect(reverse('app:tabela', args=[table_id]))
            return None

    return {'tabela': tabela, 'form': form}