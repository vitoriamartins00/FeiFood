from config import espaco

lista_alimentos = [
    {"nome": "Spaghetti Carbonara","informacoes": "Macarrão spaghetti, molho pomodoro, carne moída e parmesão ralado","preco": 38.50},  #um dicionario item na lista, com nome,preço e avaliação
    {"nome": "Lasanha Bolonhesa", "informacoes": "Massa artesanal com molho pomodoro, presunto e queijo mussarela","preco": 45.00},
    {"nome": "Pizza Margherita","informacoes": "Massa artesanal, molho de tomate fresco, mussarela de búfala e manjericão","preco": 55.00},
    {"nome": "Pizza Pepperoni", "informacoes": "Massa artesanal, molho de tomate, mussarela e fatias generosas de pepperoni" ,"preco": 62.00},
    #sobremesa
    {"nome": "Tiramisu", "informacoes": "feita com queijo mascarpone, biscoito, café e cacau em pó","preco": 23.00},
    {"nome": "Panna Cotta com Frutas","informacoes": "feita com creme de leite cozido e adoçado, servido com calda de frutas vermelhas frescas", "preco": 18.50},
    #bebidas
    {"nome": "Suco de Laranja","informacoes": "suco de laranja 100% natural, espremido na hora","preco": 12.00},
    {"nome": "Soda Italiana","informacoes":"feita com xarope de frutas, água com gás e gelo", "preco": 18.00}
]

#funcao para exibir o cardapio completo, com formatacao alinhada
def exibir_cardapio():
    print(f"\n|{'Cardápio Completo':^{espaco}}|")
    print(f"+{'-'*espaco}+")
    print(f"|{'ITEM':<50}|{'PREÇO':<14}|{'INFORMAÇÕES':<34}|")
    #percorre cada item na lista de alimentos para exibir
    for a in lista_alimentos:
        nome = a['nome']
        preco = a['preco']
        informacoes = a['informacoes']
        max_info = 34
        if len(informacoes) > max_info:
            info_resumo = informacoes[:(max_info - 3)] +'...' 
        else:
            info_resumo = informacoes
        print(f"|{nome:<50}|R$ {preco:<11.2f}|{info_resumo:<34}|") #imprime cada item com a formatação do tam fixo para manter alinhado
    print(f"+{'-' * espaco}+")

#funcao para buscar alimentos do cardapio
def buscar_alimentos():
    print(f"\n|{'Busca por Alimentos':^{espaco}}|")
    
    exibir_cardapio()

    busca = input("\nO que vai pedir hoje? ").lower() #conversão para minusculo para comparacao
    resultado_busca = []        #criando uma lista vazia para guardar os itens encontrados

    #percorre cada item da lista global 'lista_alimentos'.
    for alimento in lista_alimentos:
        #checa se busca está contido em em alimento e converte para minusculo para comparacao
        if busca in alimento["nome"].lower():
            #se encontrar item correspondente na lista adiciona a lista dos resultados
            resultado_busca.append(alimento)
    if resultado_busca == []:
        print(f"\nNenhum alimento encontrado para: '{busca}'")
        return  #encerra a funcao se nenhum resultado foi encontrado
    else:
        print(f"\n{len(resultado_busca)} resultado(s) encontrado(s) para '{busca}':")   #exibe a quantidade de resultados encontrados
        print(f"+{'-' * espaco}+")
        #percorre cada item apresentado na lista resultado_busca para formatar a exibição
        for a in resultado_busca:
            nome = a['nome']
            preco = a['preco']
            informacoes = a['informacoes']

            max_info = 89
            if len(informacoes) > max_info:
                info_resumo = informacoes[:(max_info - 3)] + '...'
            else:
                info_resumo = informacoes
            print(f"|{nome:<80}|R$ {preco:.2f}") #imprime cada item com a formatação do tam fixo para manter alinhado
            print(f"|Descrição: {info_resumo:<{max_info}}|")
        print(f"+{'-' * espaco}+")
