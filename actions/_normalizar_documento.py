from app.models import *
from app.forms import TableForm
from classes._util import gerarHash


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

            array_campos_sem_tabela = Campo_Tabela.objects.filter(tabela=tabela_base)
            campos_sem_tabela = []
            for rel in array_campos_sem_tabela:
                temp = Campo.objects.get(id=rel.campo.id)
                campos_sem_tabela.append(temp)

            array_restricoes = []
            for campo in campos_sem_tabela:
                restricoes = campo.campo_tabela_set.filter(tipo_campo='PK')
                #restricoes = campo.restricao_set.filter(tipo='PK')
                if restricoes:
                    for restricao in restricoes: array_restricoes.append(restricao.campo.id)

            if len(tabelas):
                for tabela in tabelas:
                    campos, array_restricoes = [], []#tabela.campo_set.order_by('ordem')

                    array = tabela.campo_tabela_set.all()
                    for rel in array:
                        aux = Campo.objects.get(id=rel.campo.id)
                        campos.append(aux)

                        if rel.tipo_campo == 'PK':
                            array_restricoes.append(rel.campo.id)

                    """
                    for campo in campos:
                        restricoes = campo.restricao_set.filter(tipo='PK')
                        if restricoes:
                            for restricao in restricoes: array_restricoes.append(restricao.campo.id)
                    """
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

                    temp_campos = []#tabela.campo_set.all()
                    campos_tabela = tabela.campo_tabela_set.all()
                    for rel in campos_tabela:
                        campo = Campo.objects.get(id=rel.campo.id)
                        temp_campos.append(campo)

                    campos, chaves, dependencias = [], [], []
                    for campo in temp_campos:
                        #restricoes = campo.restricao_set.filter(tipo='PK')
                        temp_restricoes = Campo_Tabela.objects.exclude(tipo_campo='FK').get(campo=campo)
                        temp_dependencias = None

                        if temp_restricoes.tipo_campo == 'PK':
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
            tabelas_renomear = documento.tabela_set.filter(renomear=True)

            array_tabelas = []
            if len(tabelas_renomear):
                for tabela in tabelas_renomear:
                    temp_rel = tabela.campo_tabela_set.all()

                    campos = []
                    for rel in temp_rel:
                        temp_campo = Campo.objects.get(id=rel.campo.id)
                        campos.append(temp_campo)

                    aux = {'tabela': tabela, 'campos': campos}
                    array_tabelas.append(aux)

                context = {'renomear_tabelas': True, 'tabelas': array_tabelas, 'documento': documento}
            else:
                tabelas = documento.tabela_set.filter(tabela_tipo=1)

                for tabela in tabelas:
                    temp_rel = tabela.campo_tabela_set.filter(tipo_campo='Normal')

                    campos = []
                    if len(temp_rel):
                        for rel in temp_rel:
                            temp_campo = Campo.objects.get(id=rel.campo.id)
                            campos.append(temp_campo)

                        aux = {'tabela': tabela, 'campos': campos}
                        array_tabelas.append(aux)

                context = {'documento': documento, 'fn': fn, 'arrayTabelas': array_tabelas}


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
                            campo_tabela = Campo_Tabela.objects.get(campo=campo)
                            campo_tabela.tipo_campo = 'PK'
                            campo_tabela.tabela = aux
                            campo_tabela.save()
                        else:
                            campo_tabela = Campo_Tabela.objects.get(campo=campo)
                            campo_tabela.tipo_campo = 'Normal'
                            campo_tabela.tabela = aux
                            campo_tabela.save()
                            #temp_restricao = Restricao(campo=campo, tipo='PK')
                            #temp_restricao.save()

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
                campos = []
                campos_tabela = tabela.campo_tabela_set.all()
                for rel in campos_tabela:
                    campo = Campo.objects.get(id=rel.campo.id)
                    campos.append(campo)

                qtde_pk = 0
                for campo in campos:
                    #chave = campo.restricao_set.filter(tipo='PK')
                    chave = campo.campo_tabela_set.filter(tipo_campo='PK')
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
            array_tabelas_eliminar = []
            for tabela in tabelas:
                chaves, campos, dependencias, array_temp = [], [], [], []

                array_campo = tabela.campo_tabela_set.all()
                for rel in array_campo:
                    temp = Campo.objects.get(id=rel.campo.id)
                    array_temp.append(temp)

                for campo in array_temp:
                    restricao = Campo_Tabela.objects.get(campo=campo)
                    #restricao = campo.restricao_set.filter(tipo='PK')
                    if restricao.tipo_campo == 'PK':
                        chaves.append(campo)
                    else:
                        campo_temp = Campo.objects.get(id=campo.id)
                        campos.append(campo_temp)
                        temp_dependencias = Dependencia.objects.filter(campo=campo)
                        dependencias.append(temp_dependencias)

                potenciais_tabelas = {}
                for chave in chaves:
                    potenciais_tabelas[chave.nome] = []

                qtde_chaves = len(chaves)
                for campo in campos:
                    qtde_dep = 0
                    for array_dep in dependencias:
                        for dep in array_dep:
                            if dep.campo == campo:
                                qtde_dep += 1

                    if qtde_chaves != qtde_dep:
                        #campos_nova_tabela.append(campo)
                        pass
                        #procura o primeiro item da dependencia
                        dep_temp = None
                        for array_dep in dependencias:
                            for dep in array_dep:
                                if dep.campo == campo:
                                    dep_temp = dep
                                    break

                        if dep_temp:
                            if dep_temp.chave.nome in potenciais_tabelas:
                                potenciais_tabelas[dep_temp.chave.nome].append(campo)

                #percorre o dicionario de novas tabelas e as cria
                for chave_nome, campos in potenciais_tabelas.items():
                    hash = gerarHash(16)
                    nova_tabela = Tabela(documento=documento, nome=hash, forma_normal=2, renomear=True)
                    nova_tabela.save()

                    #passa os campos para a nova tabela
                    for campo in campos:
                        rel = Campo_Tabela.objects.get(campo=campo, tipo_campo='Normal')
                        rel.tabela = nova_tabela
                        rel.save()

                    #cria uma chave estrangeira na nova tabela
                    chave = Campo.objects.get(nome=chave_nome)
                    rel = Campo_Tabela(campo=chave, tabela=nova_tabela, tipo_campo='FK')
                    rel.save()

                #verifica se sobrou algum campo na tabela antiga
                for tabela in tabelas:
                    chaves, campos, passar = [], [], False

                    array_chave = tabela.campo_tabela_set.filter(tipo_campo='PK')
                    array_campo = tabela.campo_tabela_set.filter(tipo_campo='Normal')

                    if len(array_campo):
                        for aux_campo in array_campo:
                            campo = Campo.objects.get(id=aux_campo.id)
                            #verifica as dependencias
                            array_dep = Dependencia.objects.filter(campo=campo)

                            if len(array_dep) == len(array_chave):
                                passar = True
                    else:
                        passar = True

                    if passar:
                        tabela.forma_normal = 2
                        tabela.save()

            context = {}
            return context
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