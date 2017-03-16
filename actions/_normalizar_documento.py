from app.models import *
from app.forms import TableForm


def run_normalizar_documento(request, documento_id):
    if request.method != 'POST':
        documento = Documento.objects.get(id=documento_id)

        #pega outras tabela e seus campos
        tabelas = documento.tabela_set.exclude(nome='tabela_base')
        nomes_tabelas, fn, arrayTabelas = '', 3, []

        if len(tabelas):
            for tabela in tabelas:
                if tabela.forma_normal < fn:
                    fn = tabela.forma_normal
        else:
            fn = 0

        if fn == 0:
            # pega os campos sem tabela
            tabela_base = documento.tabela_set.get(nome='tabela_base', tabela_tipo=0)
            tabela_base.nome = documento.nome

            campos_sem_tabela = tabela_base.campo_set.order_by('ordem')

            array_restricoes = []
            for campo in campos_sem_tabela:
                restricoes = campo.restricao_set.filter(tipo='PK');
                if restricoes:
                    for restricao in restricoes: array_restricoes.append(restricao.campo.id)

            if len(tabelas):
                for tabela in tabelas:
                    campos = tabela.campo_set.order_by('ordem')
                    array_restricoes = []
                    for campo in campos:
                        restricoes = campo.restricao_set.filter(tipo='PK');
                        if restricoes:
                            for restricao in restricoes: array_restricoes.append(restricao.campo.id)

                    #chaves = tabela.campo_set.filter(primary=True)
                    aux = {'tabela': tabela, 'campos': campos, 'restricoes_pk': array_restricoes}
                    arrayTabelas.append(aux)
                    nomes_tabelas += tabela.nome+'666'
            else:
                arrayTabelas.append({'tabela': tabela_base, 'campos': campos_sem_tabela, 'restricoes_pk': array_restricoes})

            tabela_form = TableForm()
            context = {'documento': documento, 'sem_tabela': campos_sem_tabela, 'arrayTabelas': arrayTabelas, 'tabela_form': tabela_form, 'nomes': nomes_tabelas, 'fn': fn}

        elif fn == 1:#FN2

            for tabela in tabelas:
                if tabela.forma_normal == 1:
                    temp_campos = tabela.campo_set.all()

                    campos, chaves, dependencias = [], [], []
                    for campo in temp_campos:
                        restricoes = campo.restricao_set.filter(tipo='PK');
                        temp_dependencias = None

                        if restricoes:
                            chaves.append(campo)
                        else:
                            campos.append(campo)
                            temp_dependencias = Dependencia.objects.filter(campo=campo)

                        if temp_dependencias:
                            for dep in temp_dependencias:
                                dependencias.append(dep)

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
                    aux = Tabela.objects.get(nome=tab['nome'])
                except Tabela.DoesNotExist:
                    aux = Tabela(nome=tab['nome'], documento=documento, tabela_tipo=1)
                    aux.save()

                if tab['campos']:
                    for c in tab['campos']:
                        nome = c['nome'].split('[')

                        try:
                            campo = Campo.objects.get(nome=nome[0])
                        except Campo.DoesNotExist:
                            campo = Campo(nome=nome[0], order=1)

                        campo.tabela = aux
                        #campo.primary = True if c['primaria'] else False
                        campo.save()
                        if c['primaria']:
                            tab['primaria'] += 1
                            temp_restricao = Restricao(campo=campo, tipo='PK')
                            temp_restricao.save()

            flag_fn = True
            for tab in tabs:
                if tab['primaria'] == 0:
                    flag_fn = False
                    break

            if flag_fn:
                for tab in tabs:
                    aux = Tabela.objects.get(nome=tab['nome'])
                    aux.forma_normal = 1
                    aux.save()

            documento = Documento.objects.get(id=documento_id)
            tabelas = documento.tabela_set.filter(tabela_tipo=1)

            for tabela in tabelas:
                campos = tabela.campo_set.all()

                qtde_pk = 0
                for campo in campos:
                    chave = campo.restricao_set.filter(tipo='PK')
                    if chave:
                        qtde_pk += 1

                if qtde_pk == 1:
                    tabela.forma_normal = 2
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
                    array_nome = chave.split('_')
                    nome = ''
                    for i, temp in enumerate(array_nome):
                        if i == len(array_nome)-2:
                            break
                        nome += temp+'_'

                    campo = Campo.objects.get(nome=nome[0:-1])

                    if nome not in ja_atualizados:
                        ja_atualizados.append(nome)
                        dep_del = Dependencia.objects.filter(campo=campo)
                        for dep in dep_del:
                            dep.delete()

                    aux_chave = Campo.objects.get(nome=valor)

                    temp = Dependencia(campo=campo, chave=aux_chave)
                    temp.save()

            """
                VERIFICA CAMPOS QUE NÃO DEPENDEM DA CHAVE INTEIRA
                CRIA UMA NOVA TABELA PARA ESSES CAMPOS
            """
            documento = Documento.objects.get(id=documento_id)
            tabelas = documento.tabela_set.filter(tabela_tipo=1, forma_normal=1)

            #MONTA UM ARRAY COM OS CAMPOS NORMAIS E UM COM AS CHAVES PRIMARIAS
            for tabela in tabelas:
                chaves, campos, dependencias = [], [], []

                array_temp = tabela.campo_set.all()
                for campo in array_temp:
                    restricao = campo.restricao_set.filter(tipo='PK')
                    if restricao:
                        chaves.append(campo)
                    else:
                        campos.append(campo)
                        temp_dependencias = Dependencia.objects.filter(campo=campo)
                        dependencias.append(temp_dependencias)

                campos_nova_tabela = []

                qtde_chaves = len(chaves)
                for campo in campos:
                    qtde_dep = 0
                    for dep in dependencias:
                        if dep.campo == campo:
                            qtde_dep += 1

                    if qtde_chaves != qtde_dep:
                        campos_nova_tabela.append(campo)
            """
                TERMINAR AQUI
            """

            """
            cont_nome = 0
            for tabela in tabelas:
                chaves, campos = [], []
                array_temp = tabela.campo_set.all()

                for campo in array_temp:
                    restricao = campo.restricao_set.filter(tipo='PK')
                    if restricao:
                        chaves.append(campo)
                    else:
                        campos.append(campo)

                nova_tabela = Tabela(forma_normal=2, documento=documento)
                flag_tabela = False

                for campo in campos:
                    dependencias = Dependencia.objects.filter(campo=campo)
                    cont = 0

                    for dependencia in dependencias:
                        for chave in chaves:
                            if dependencia.chave == chave:
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
                            fk = Restricao(campo=campo, tipo='FK')
                            fk.save()

                #tabela.forma_normal = 2
                #tabela.save()
            """
            context = {}
            return context