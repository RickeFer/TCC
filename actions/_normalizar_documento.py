from app.models import *
from app.forms import TableForm


def run_normalizar_documento(request, documento_id):
    if request.method != 'POST':
        documento = Documento.objects.get(id=documento_id)

        #pega outras tabela e seus campos
        tabelas = documento.table_set.exclude(name='tabela_base')
        nomes_tabelas, fn, arrayTabelas = '', 3, []

        if len(tabelas):
            for tabela in tabelas:
                if tabela.normal_form < fn:
                    fn = tabela.normal_form
        else:
            fn = 0

        print(tabelas)

        if fn == 0:
            # pega os campos sem tabela
            tabela_base = documento.table_set.get(name='tabela_base', type_table=0)

            campos_sem_tabela = tabela_base.field_set.order_by('order')
            if len(tabelas):
                for tabela in tabelas:
                    campos = tabela.field_set.order_by('order')
                    chaves = tabela.field_set.filter(primary=True)
                    aux = {'tabela': tabela, 'campos': campos, 'chaves': chaves}
                    arrayTabelas.append(aux)
                    nomes_tabelas += tabela.name+'666'
            else:
                arrayTabelas.append({'tabela': tabela_base, 'campos': campos_sem_tabela})

            tabela_form = TableForm()
            context = {'documento': documento, 'sem_tabela': campos_sem_tabela, 'arrayTabelas': arrayTabelas, 'tabela_form': tabela_form, 'nomes': nomes_tabelas, 'fn': fn}
        elif fn == 1:
            for tabela in tabelas:
                chaves = tabela.field_set.filter(primary=True)

                if len(chaves) > 1:
                    campos = tabela.field_set.order_by('order')

                    dependencias = []
                    for campo in campos:
                        if campo.primary == False:
                            dependencias = Dependencia.objects.filter(campo=campo)


                    aux = {'tabela': tabela, 'campos': campos, 'chaves': chaves, 'dependencias': dependencias}
                    arrayTabelas.append(aux)
                    #nomes_tabelas += tabela.name + '666'

            context = {'documento': documento, 'arrayTabelas': arrayTabelas, 'fn': fn}
        elif fn == 2:
            context = {'documento': documento, 'fn': fn}

        return context
    else:
        aux = request.POST


        if aux['forma_normal'] == '1':
            """
                DEFINE AS TABELAS
            """
            tabs = []
            maior = 0
            for p in aux:
                if p[:6] == 'tabela':
                    nome = p[7:]
                    temp = {'nome': nome, 'ordem': -1, 'bottom': -1, 'primaria': False}
                    temp['top'] = request.POST[nome + "_top"]
                    tabs.append(temp)
                    if float(temp['top']) > maior:
                        maior = float(temp['top'])

            """
                DEFINE A ORDEM DAS TABELAS E SUAS POSICOES
            """
            cont = 0
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

            documento = Documento.objects.get(id=documento_id)



            for tab in tabs:
                if tab['nome'] == 'sem_tabela':
                    tab['nome'] = documento.name
                try:
                    aux = Tabela.objects.get(name=tab['nome'])
                except Tabela.DoesNotExist:
                    aux = Tabela(name=tab['nome'], document=documento, type_table=1)
                    aux.save()

                if tab['campos']:
                    for c in tab['campos']:
                        nome = c['nome'].split('[')

                        try:
                            campo = Campo.objects.get(name=nome[0])
                        except Campo.DoesNotExist:
                            campo = Campo(name=nome[0], order=1)

                        campo.tabela = aux
                        campo.primary = True if c['primaria'] else False
                        if campo.primary:
                            tab['primaria'] = True
                        campo.save()

            flag_fn = True
            for tab in tabs:
                if tab['primaria'] != True:
                    flag_fn = False
                    break

            if flag_fn:
                for tab in tabs:
                    aux = Tabela.objects.get(name=tab['nome'])
                    aux.normal_form = 1
                    aux.save()

            documento = Documento.objects.get(id=documento_id)
            tabelas = documento.table_set.filter(type_table=1)

            for tabela in tabelas:
                chaves = tabela.field_set.filter(primary=True)
                if len(chaves) == 1:
                    tabela.normal_form = 2
                    tabela.save()

            context = {'post': tabs}
            return context

        elif aux['forma_normal'] == '2':

            """
                SALVA AS DEPENDENCIAS
            """
            campos, ja_atualizados = [], []
            for chave, valor in aux.items():
                aux_nome = chave[:-15:-1]; aux_nome = aux_nome[::-1]; aux_nome = aux_nome[1:12]

                if aux_nome == 'dependencia':
                    nome = chave.split('_'); nome = nome[0]
                    campo = Campo.objects.get(name=nome)

                    if nome not in ja_atualizados:
                        ja_atualizados.append(nome)
                        dep_del = Dependencia.objects.filter(campo=campo)
                        for dep in dep_del:
                            dep.delete()

                    aux_chave = Campo.objects.get(name=valor)

                    temp = Dependencia(campo=campo, dependente=aux_chave)
                    temp.save()

            """
                VERIFICA CAMPOS QUE NÃO DEPENDEM DA CHAVE INTEIRA
                CRIA UMA NOVA TABELA PARA ESSES CAMPOS
            """
            documento = Documento.objects.get(id=documento_id)
            tabelas = documento.table_set.filter(type_table=1, normal_form=1)

            cont_nome = 0
            for tabela in tabelas:
                chaves = tabela.field_set.filter(primary=True)
                campos = tabela.field_set.filter(primary=False)

                nova_tabela = Tabela(normal_form=2, document=documento)
                flag_tabela = False

                for campo in campos:
                    dependencias = Dependencia.objects.filter(campo=campo)
                    cont = 0

                    for dependencia in dependencias:
                        for chave in chaves:
                            if dependencia.dependente == chave:
                                cont += 1

                    if len(chaves) > cont:
                        if flag_tabela == False:
                            nova_tabela.nome = 'nova_tabela_' + str(cont_nome)
                            nova_tabela.forma_normal = 2
                            nova_tabela.save()
                            cont_nome += 1
                            flag_tabela = True

                        campo.table = nova_tabela
                        campo.save()

                        for dependencia in dependencias:
                            fk = ChaveEstrangeira(tabela=tabela, campo=dependencia.dependente)
                            fk.save()

                tabela.normal_form = 2
                tabela.save()

            context = {}
            return context