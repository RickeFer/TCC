from app.models import *
from app.forms import TableForm


def run_normalizar_documento(request, documento_id):
    if request.method != 'POST':
        documento = Document.objects.get(id=documento_id)

        #pega os campos sem tabela
        tabela_base = documento.table_set.get(name=documento.name)
        campos_sem_tabela = tabela_base.field_set.order_by('order')

        arrayTabelas = []
        #pega outras tabela e seus campos
        tabelas = documento.table_set.exclude(name=documento.name)
        for tabela in tabelas:
            campos = tabela.field_set.order_by('order')
            aux = {'tabela': tabela, 'campos': campos}
            arrayTabelas.append(aux)

        tabela_form = TableForm()

        context = {'documento': documento, 'sem_tabela': campos_sem_tabela, 'arrayTabelas': arrayTabelas, 'tabela_form': tabela_form}
        return context
    else:
        aux = request.POST

        """
            DEFINE AS TABELAS
        """
        tabs = []
        maior = 0
        for p in aux:
            if p[:6] == 'tabela':
                nome = p[7:]
                temp = {'nome': nome, 'ordem': -1, 'bottom': -1}
                temp['top'] = request.POST[nome + "_top"]
                tabs.append(temp)
                if float(temp['top']) > maior:
                    maior = float(temp['top'])

        """
            DEFINE A ORDEM DAS TABELAS E SUAS POSICOES
        """
        cont = 0;
        temp = []
        while cont < len(tabs):
            for tab in tabs:
                if float(tab['top']) == maior:
                    tab['ordem'] = cont
                    cont += 1
                    temp.append(tab)
                    break

            maior = 0
            for tab in tabs:
                if float(tab['top']) > maior and tab['ordem'] == -1:
                    maior = float(tab['top'])
        tabs = temp

        tops = []
        for p in aux:
            temp = p.split("'")
            if 'top' in temp:
                # print(aux[p])
                nome = p.split('[')[0]
                primaria = False

                try:
                    if request.POST[nome+'[primaria]'] == '1':
                        primaria = True #request.POST[nome+'[primaria]']
                except:
                    pass

                temp = {'tipo': 'campo', 'nome': p, 'top': aux[p], 'primaria': primaria}
                tops.append(temp)
        # fecha o range da tabela
        for i in reversed(range(len(tabs))):
            if i == 0:
                continue
            tabs[i]['bottom'] = tabs[i - 1]['top']

        """
            DISTRIBUI OS CAMPOS EM SUAS TABELAS
        """
        for tab in tabs:
            temp = []
            for camp in tops:
                if int(camp['top']) >= int(tab['top']):
                    if int(tab['bottom']) == -1:
                        temp.append(camp)
                    elif int(camp['top']) <= int(tab['bottom']):
                        temp.append(camp)
            tab['campos'] = temp

        documento = Document.objects.get(id=documento_id)


        for tab in tabs:
            if tab['nome'] == 'sem_tabela':
                tab['nome'] = documento.name
            try:
                aux = Table.objects.get(name=tab['nome'])
            except Table.DoesNotExist:
                aux = Table(name=tab['nome'], document=documento, type_table=1)
                aux.save()

            if tab['campos']:
                for c in tab['campos']:
                    nome = c['nome'].split('[')

                    try:
                        campo = Field.objects.get(name=nome[0])
                    except Field.DoesNotExist:
                        campo = Field(name=nome[0], order=1)

                    campo.table = aux
                    campo.primary = True if c['primaria'] else False
                    campo.save()

        context = {'post': tabs}
        return context