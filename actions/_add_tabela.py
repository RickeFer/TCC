from app.forms import TableForm
from app.models import *


def runAdd_tabela(request):
    if request.method != 'POST':
        form = TableForm()
    else:
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse('app:tabelas'))
            return None

    return {'form': form}