from config import lista_pedidos, espaco, opcao_gerenc_pedido, prox_id_pedido

from cardapio import lista_alimentos, exibir_cardapio

#funcao que carrega os dados dos pedidos do arquivo para a lista 'lista_pedidos'
def historico_pedido():
    global lista_pedidos #vamos modificar a lista global 
    global prox_id_pedido
    lista_pedidos.clear()   #limpa a lista atual antes de carregar e evita duplicação
    maior_id = 0
    try:
        with open('pedidos.txt', 'r') as pedidos:
            for linha in pedidos:
                linha = linha.strip()   
                if not linha:   #verifica se a linha está vazia
                    continue    #ignora as linhas vazias

                dados_pedido = linha.split(',') #separa a linha em uma lista de 5 partes (id,e-mail,total,avaliacao,sacola_formata)
                
                if len(dados_pedido) != 5:
                    print(f"Alerta: Erro na linha do pedido: {linha}")  #alerta se a linha for diferente de 5, se não tiver 5 partes
                    continue

                id_pedido_str = dados_pedido[0].strip()
                id_usuario_str = dados_pedido[1].strip()
                valor_total_str = dados_pedido[2].strip()
                avaliacao_pedido_str = dados_pedido[3].strip()
                sacola_format =  dados_pedido[4].strip()

                if id_pedido > maior_id:
                    maior_id = id_pedido

                try:
                    id_pedido = int(id_pedido_str)
                    valor_total = float(valor_total_str)
                    avaliacao_pedido = float(avaliacao_pedido_str)
                except ValueError as ve:
                    # se falhar, imprime a linha inteira e o erro específico
                    print(f"Erro de conversão na linha: {linha}")
                    print(f"Problema: {ve}")
                    continue # pula esta linha corrompida

                itens_sacola = []   #cria uma lista temporaria para reconstruir o dicionario de itens
                itens_str = sacola_format.split('|')

                for item_str in itens_str:  #loop que percorre cada string de item na sacola formatada
                    item_str = item_str.strip()
                    if not item_str:      #verifica se a string está vazia
                        continue            

                    dados_item = item_str.split('-') #separa a string do item em partes (nome,preço,avaliacao)   

                    if len(dados_item) == 2:
                        nome_item = dados_item[0].strip()
                        preco_item_str = dados_item[1].strip()
                        
                        try:
                            # tenta converter o preço do item
                            preco_item = float(preco_item_str)
                        except ValueError as ve_item:
                            print(f"Erro de conversão do item: {nome_item} na linha: {linha}")
                            print(f"Preço Incorreto: '{preco_item_str}'")
                            continue 
                            
                        item_pedido = {
                            "nome": nome_item,
                            "preco": preco_item,
                            "avaliacao": 0.0
                        }
                        itens_sacola.append(item_pedido)    #adiciona o dicionario do item a lista temporaria

                #convertendo os dados do dicionario        
                novo_pedido = {
                    "id_pedido": id_pedido,
                    "id_usuario": id_usuario_str,
                    "valor_total": valor_total,
                    "avaliacao": avaliacao_pedido,    #avaliacao do pedido
                    "sacola": itens_sacola
                }
                lista_pedidos.append(novo_pedido)
    except FileNotFoundError:   #se o arquivo não existir, apenas ignora e mantém a lista vazia
        pass
    except Exception as e:  #captura qualquer outro erro
        print(f"Erro ao carregar histórico de pedidos: {e}")

    if maior_id == 0 and lista_pedido == []:
        prox_id_pedido = 1
    else:
        prox_id_pedido = maior_id + 1


#funcao para salvar os dados dos pedidos no arquivo
def salvar_pedido():
    try:
        with open('pedidos.txt', 'w') as pedidos:
            for pedido in lista_pedidos:    #loop que percorre cada dicionario de pedido na lista 'lista_pedidos'
                itens_sacola = []           #cria uma lista temporaria para formatar os itens dentro da sacola
                for item in pedido['sacola']:   #loop que percorre os itens dentro da lista 'sacola' do pedido atual
                    #pegando os valores do dicionario e convertendo para string para salvar no arquivo que só aceita string
                    nome = item['nome']
                    preco = str(item['preco'])

                    #pegando a string de cada item do pedido e juntando
                    item_pedido = nome + '-' + preco
                    itens_sacola.append(item_pedido)    #adiciona a string formatada a lista temporaria 

                sacola_format = "|".join(itens_sacola)  #junta todas as strings de itens_sacola em uma unica 

                #linha final do pedido completa
                pedido_completo = f"{pedido['id_pedido']},{pedido['id_usuario']},{pedido['valor_total']},{pedido['avaliacao']},{sacola_format}\n"
                pedidos.write(pedido_completo)  #escreve a linha completa no arquivo
    except IOError:   #tratamento do caso de não conseguir salvar o arquivo
        print("Erro ao salvar o pedido.")

#funcao calcular total do pedido
def calcular_total(pedido):
    total = 0.0  #inicializa o total 
    for item in pedido['sacola']:
        preco_item = item['preco']
        total += preco_item 
    pedido['valor_total'] = total
    return total

#funcao auxiliar que adiciona item ao pedido durante a edicao
def adicionar_item(pedido):
    exibir_cardapio()   #chama a funcao para exibir o cardapio para que o usuario saiba o que digitar
    nome_item = input("Digite o NOME exato do item para adicionar: ").lower()
    item_encontrado = None  #variável de controle para verificar se o item foi encontrado
    #busca o item na lista de alimentos
    for alimento in lista_alimentos:
        if alimento['nome'].lower() == nome_item:
            item_encontrado = alimento  #se encontrar armazena o dicionario do item encontrado
            break

    if item_encontrado:
        #se o item foi encontrado, adiciona uma cópia do dicionario do alimento na sacola do pedido
        pedido['sacola'].append(item_encontrado.copy())
        print(f"'{item_encontrado['nome']}' adicionado!")
        pedido['valor_total'] = calcular_total(pedido)  #atualiza o valor total do pedido
        print(f"Novo total do pedido: R$ {pedido['valor_total']:.2f}")
    else:
        print(f"'{nome_item}' não encontrado no cardápio.")

#funcao auxiliar que remove item do pedido durante a edicao
def remover_item(pedido):
    if not pedido['sacola']: #se a sacola estiver vazia
        print("A sacola está vazia.")
        return
    
    print("\n--- Itens atuais na sacola ---")
    #exibe os itens na sacola, mostrando o indice e o nome
    for indice, item in enumerate(pedido['sacola']):
        print(f"[{indice}] {item['nome']} - R$ {item['preco']:.2f}")
    
    nome_item = input("Digite o NOME exato do item que deseja remover: ").lower().strip()
    item_removido = None    #variável de controle para verificar se o item foi removido

    #busca o item na sacola, obtendo o indice e o item do dicionario sacola
    for i, item_dic in enumerate(pedido['sacola']):
        #se o nome do item na sacola é igual ao nome digitado
        if item_dic['nome'].lower() == nome_item:
            item_removido = pedido['sacola'].pop(i)
            break
    if not item_removido:   #se item não tem valor ou não foi localizado na sacola
        print(f"'{nome_item}' não encontrado na sacola.")
        return
    else: #senao o item tem valor, e foi removido com sucesso
        print(f"'{item_removido['nome']}' removido com sucesso!")

        pedido['valor_total'] = calcular_total(pedido)  #atualiza o valor total do pedido
        print(f"Novo total do pedido: R$ {pedido['valor_total']:.2f}")

#funcao para criar um novo pedido   
def criar_novo_pedido(usuario_logado):
    global prox_id_pedido
    global lista_pedidos
    print(f"\n|{'Criar novo pedido':^{espaco}}|")
    itens_pedido = []   #cria lista temporaria para armazenar os itens do pedido

    exibir_cardapio()   #chama a funcao que mostra o cardapio completo para o usuario

    while True:
        pedido = input("\nDigite o nome EXATO do alimento para adicionar ao pedido ou 'FIM' para encerrar: ")
        #se o usuario escolher finalizar o pedido o loop é encerrado
        if pedido.upper() == 'FIM':
            break   

        #tenta encontrar o item buscado no cardapio
        pedido_encontrado = None    #variável de controle para verificar se o item foi encontrado, e None porque isso indica que nenhum item foi encontrado ainda.
        for alimento in lista_alimentos: #percorre cada dic de alimento na lista
            if alimento['nome'].lower() == pedido.lower():
                pedido_encontrado = alimento
                break
        if pedido_encontrado:
            #cria uma copia, para que a alteracao do item, nao altere o cardapio original
            item_do_pedido = pedido_encontrado.copy()
            itens_pedido.append(item_do_pedido) #sacola do usuario recebe a variavel da copia
            total_parcial = calcular_total({'sacola':itens_pedido})
            print(f"Item '{item_do_pedido['nome']}' adicionado! Total da compra: R${total_parcial:.2f}")
        else:
            print("Item não encontrado.")
    if itens_pedido == []:  #se a lista de itens do pedido estiver vazia
        print("\nPedido cancelado. Nenhum item adicionado.")
        return
    
    total_final = calcular_total({'sacola':itens_pedido})
    
    #dicionario do novo pedido
    novo_pedido = {
        "id_pedido": prox_id_pedido, #criando id do pedido com contador
        "id_usuario": usuario_logado['e-mail'], #acessando o usuario pelo e-mail para salvar avaliação
        "sacola": itens_pedido,
        "valor_total": total_final,
        "avaliacao": 0.0
    }

    prox_id_pedido += 1
    lista_pedidos.append(novo_pedido) #adiciona o novo pedido a lista global
    salvar_pedido()                   #chama a funcao para salvar o pedido no arquivo

    #mensagem de validação do pedido criado
    print(f"+{'-' * espaco}+")
    print(f"Pedido #{novo_pedido['id_pedido']} Criado com sucesso!")
    print(f"Valor Total: R$ {total_final:.2f}")
    print(f"+{'-' * espaco}+")

#funcao auxiliar para exibir os pedidos do usuario (usada em avaliar, editar e excluir)
def exibir_pedidos(pedidos_lista,espaco):
    print(f"+{'-' * espaco}+")
    print(f"|{'Seus Pedidos':^{espaco}}|")
    print(f"+{'-' * espaco}+")

    #para pedido na lista de pedidos do usuario
    for pedido in pedidos_lista:
        #verifica se o pedido já foi avaliado
        if pedido['avaliacao'] > 0:
            status_avaliacao = "Já avaliado"
        else:
            status_avaliacao = "PENDENTE"

        #formatação da exibição do pedido
        txt_id_valor = (f"ID: {pedido['id_pedido']}|Valor: R$ {pedido['valor_total']:.2f}")
        txt_aval_status = (f"Avaliação: {pedido['avaliacao']:.1f}")
        print()
        print(f"{txt_id_valor:<10}|{txt_aval_status:>25}|Status da Avaliação: {status_avaliacao:^20}")
        print()
    print(f"+{'-' * espaco}+")

#funcao para editar um pedido existente
def editar_pedido(usuario_logado):
    global lista_pedidos    #declarando que a lista global será modificada
    print(f"\n{'Editar Pedido':^{espaco}}")
    email_usuario = usuario_logado['e-mail']
    pedido_usuario = []  #lista temporaria para armazenar os pedidos do usuario logado
    #filtra os pedidos pertencentes ao usuario logado
    for p in lista_pedidos: #para cada pedido na 'lista_pedidos'
        #se o id_usuario do pedido for igual ao e-mail do usuario logado, adiciona a lista temporaria
        if p['id_usuario'] == email_usuario:
            pedido_usuario.append(p)
    if not pedido_usuario:  #se a lista temporaria estiver vazia
        print("Você não possui pedidos para editar.")
        return
    
    #chamando a funcao para exibir os pedidos do usuario com formatação para escolha
    exibir_pedidos(pedido_usuario,espaco)
    try:
        id_editar = int(input("Digite o ID do pedido que deseja editar (ou 0 para cancelar): "))
    except ValueError:      
        print("ID inválido. Tente novamente.")
        return
    if id_editar == 0:
        return
    
    pedido_editar = None
    indice_pedido = -1  #inicializa o índice do pedido como -1 (indicando que não foi encontrado)

    #busca o pedido pelo id a ser editado na lista global. 
    for indice, pedido in enumerate(lista_pedidos):
        if pedido['id_pedido'] == id_editar and pedido['id_usuario'] == email_usuario:
            pedido_editar = pedido  #armazena o dicionario do pedido a ser editado
            indice_pedido = indice  #guarda o índice do pedido na lista global
            break
    #se o pedido não foi encontrado
    if not pedido_editar:
        print(f"Pedido com ID{id_editar} não encontrado.")
        return
    
    #menu de edição do pedido, enquanto o usuario não finalizar a edição
    while True:
        print(f"\n---Editando Pedido #{id_editar}---")
        print(f"Valor Atual: R${pedido_editar['valor_total']:.2f}")

        print(f"\nItens Atuais na Sacola:")
        if not pedido_editar['sacola']:
            print("Sacola vazia.")
        else:
            #exibe os itens na sacola com índice, nome e preço
            for i, item in enumerate(pedido_editar['sacola']):
                print(f"[{i}] {item['nome']} - R$ {item['preco']:.2f}")

        print("\n1: Adicionar novo item")
        print("2: Remover item")
        print("0: Finalizar Edição")

        opcao_edicao = input("Escolha uma das opções: ")

        if opcao_edicao == '0':
            break   #sai do loop de edição
        elif opcao_edicao == '1':
            adicionar_item(pedido_editar)   #chama a funcao para adicionar item
        elif opcao_edicao == '2':
            remover_item(pedido_editar)   #chama a funcao para remover item
        else:
            print("Opção inválida.")

    pedido_editar['valor_total'] = calcular_total(pedido_editar)#chama a funcao para recalcular o valor total do pedido
    salvar_pedido() #chama a funcao para salvar as alterações no arquivo

    print(f"\nPedido #{id_editar} editado e salvo com sucesso!")
    print(f"\nNovo total: R$ {pedido_editar['valor_total']:.2f}")

#funcao para excluir pedido existente
def excluir_pedido(usuario_logado):
    global lista_pedidos    #declarando que a lista global será modificada
    print(f"\n{'Excluir Pedido':^{espaco}}")
    email_usuario = usuario_logado['e-mail']
    pedidos_usuario = []    #lista temporaria para armazenar os pedidos do usuario logado
    #filtra os pedidos pertencentes ao usuario logado
    for p in lista_pedidos: #para cada pedido na 'lista_pedidos'
        #se o id_usuario do pedido for igual ao e-mail do usuario logado, adiciona a lista temporaria
        if p['id_usuario'] == email_usuario:
            pedidos_usuario.append(p)
    if not pedidos_usuario: #se a lista temporaria estiver vazia
        print("Você não possui pedidos para excluir.")
        return
    #chamando a funcao para exibir os pedidos do usuario com formatação para escolha
    exibir_pedidos(pedidos_usuario,espaco)
    
    try:
        id_excluir = int(input("Digite o ID do pedido que deseja excluir (ou 0 para cancelar): "))
    except ValueError:
        #se o ID for inválido, exibe a mensagem e encerra a funcao
        print("ID inválido.")
        return
    
    #se o usuario optar por cancelar a exclusão retorna ao menu anterior
    if id_excluir == 0:
        return
    
    #busca o pedido pelo id a ser excluído na lista global.
    pedido_encontrado = None
    #percorre a lista global de pedidos com índice, busca o pedido a ser excluído
    for indice, pedido in enumerate(lista_pedidos):
        #verifica se o id do pedido e o id do usuario correspondem
        if pedido['id_pedido'] == id_excluir and pedido['id_usuario'] == email_usuario:
            pedido_encontrado = lista_pedidos.pop(indice) #remove o pedido da lista global
            break
    if pedido_encontrado:
        salvar_pedido() #chama a funcao para salvar as alterações no arquivo
        print(f"\nPedido #{id_excluir} excluído com sucesso!")
    else:   #se o pedido não foi encontrado
        print(f"Pedido com ID #{id_excluir} não encontrado.")

#funcao para avaliar um pedido existente
def avaliar_pedido(usuario_logado):
    print(f"\n| {'Avaliar Pedido':^{espaco}}|")
    email_usuario = usuario_logado['e-mail']
    pedidos_usuario = []    #lista temporaria para armazenar os pedidos do usuario logado

    #filtra os pedidos pertencentes ao usuario logado
    for pedido in lista_pedidos:
        if pedido['id_usuario'] == email_usuario:
            pedidos_usuario.append(pedido)
    if not pedidos_usuario: #se a lista temporaria estiver vazia
        print("Você não possui pedidos para avaliar.")
        return
    #chamando a funcao para exibir os pedidos do usuario com formatação para escolha
    exibir_pedidos(pedidos_usuario,espaco)

    try:
        id_escolhido = int(input("Digite o ID do pedido que deseja avaliar (ou 0 para cancelar): "))
    except ValueError:
        print("ID inválido. Tente novamente.")
        return

    if id_escolhido == 0:
        return
    #inicializando variavel para armazenar o pedido a ser avaliado, none porque ainda não foi encontrado
    pedido_avaliacao = None
    #busca o pedido pelo id a ser avaliado na lista global
    for p in lista_pedidos:
        if p['id_pedido'] == id_escolhido and p['id_usuario'] == email_usuario:
            pedido_avaliacao = p    #encontrou o dicionario do pedido
            break
    if pedido_avaliacao is None:    #se o pedido não foi encontrado
        print(f"Pedido com ID {id_escolhido} não encontrado.")
        return

    #coleta a nota de avaliação do pedido
    while True:
        try:
            nota = float(input(f"Atribua a nota ao pedido {id_escolhido} (0 a 5 estrelas): "))
            if 0.0 <= nota <= 5.0:  #verifica se a nota está no intervalo válido
                break
            else:
                print("A nota deve estar no intervalo entre 0 e 5.")
        except ValueError:
            print("Nota inválida. Digite um número.")
    #atribui a nota ao campo 'avaliacao' do pedido
    pedido_avaliacao['avaliacao'] = nota    

    salvar_pedido() #chama a funcao para salvar as alterações no arquivo
    print(f"\nPedido {id_escolhido} avaliado com sucesso! Nota: {nota:.1f} estrelas.")

#funcao que gerencia o menu de pedidos (todas as ações relacionadas a pedidos)
def gerenciamento_pedido(usuario_logado):
    while True:
        #exibição do menu de gerenciamento de pedidos
        print(f"+{'-'* espaco}+")
        print(f"|{"Gerenciamento de Pedidos":^{espaco}}|")
        print(f"+{'-'*espaco}+")
        for k,v in opcao_gerenc_pedido.items():
            print(f"|{f'{k} : {v}':{espaco}}|")
        print(f"+{'-' * espaco}+")
        #recebe a opção do usuário
        try:
            ops_func_pedido = int(input("Digite o número que corresponde a opção desejada: "))
        except ValueError:
            print("Opção inválida, por favor digite o número correspondente a uma das funcionalidades apresentada: ")
            continue    #volta ao inicio do loop
        
        #verifica e executa a funcao escolhida
        if ops_func_pedido in opcao_gerenc_pedido:
            if ops_func_pedido == 0:
                break   #volta para o menu_apos_login
            elif ops_func_pedido == 1:
                editar_pedido(usuario_logado) 
            elif ops_func_pedido == 2:
                excluir_pedido(usuario_logado)  
        else:
            print("Opção inválida.")

