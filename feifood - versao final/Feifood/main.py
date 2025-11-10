from usuario import ler_usuarios, login_usuario, cadastro_usuario, remover_usuario
from pedido import historico_pedido,criar_novo_pedido, gerenciamento_pedido, avaliar_pedido, calcular_total
from cardapio import buscar_alimentos, exibir_cardapio, lista_alimentos
from config import lista_usuarios, lista_pedidos,espaco, opcoes,opcoes_usuario, opcao_gerenc_pedido

#funcao do menu apos o login do usuario 
def menu_apos_login(usuario_logado):
    while True: #mantém o usuario no menu até que ele saia 
        print(f"+{"-" * espaco}+")
        print(f"\n|{"HOME":^{espaco}}|")
        #mostra as opções listando os itens do dicionario
        for k,v in opcoes_usuario.items():
            print(f"|{f'{k}: {v}':{espaco}}|")
        print(f"+{"-" * espaco}+")
        #recebe a opcao e trata erros
        try:
            ops = int(input())
        except ValueError:
            print("Opção inválida, por favor digite o número correspondente a uma das opções apresentada: ")
            continue
        #verifica e executa a funcao escolhida
        if ops in opcoes_usuario:
            if ops == 0:
                print("Encerrando seu acesso. Até logo!")
                break   #sai do loop e retorna ao menu principal
            elif ops == 1:
                buscar_alimentos()  #chama a funcao de busca por alimentos
            elif ops == 2:
                criar_novo_pedido(usuario_logado)
            elif ops == 3:
                gerenciamento_pedido(usuario_logado)    #chama a funcao menu de gerenciamento
            elif ops == 4:
                avaliar_pedido(usuario_logado)
            elif ops == 5:
                remover_usuario(usuario_logado)
                if remover_usuario:
                    break
        else:
            print("Opção inválida.") 

#funcao principal que chama o menu inicial - login/cadastro/sair
def menuPrincipal():

    #carrega os dados salvos antes de tudo e preenche as listas
    ler_usuarios()
    historico_pedido()

    while True:
        #exibição do menu
        print(f"+{'-' * espaco}+")
        print(f"|{"FeiFood":^{espaco}}|") #centraliza o menu
        print(f"+{'-' * espaco}+")
        for k,v in opcoes.items():
            print(f"|{f'{k} : {v}':{espaco}}|")
        print(f"+{'-' * espaco}+")
        
        try:
            op = int(input())
        except ValueError:
            print("Por favor digite uma das opções: ")
            continue

        #validacao das opcoes existentes
        if op in opcoes:
            if op == 1:
                #chama a funcao e captura o valor retornado (usuario_logado ou none)
                usuario_logado = login_usuario()
                #se foi realizado com sucesso (retorna um dicionario e não é none)
                if usuario_logado is not None:  
                    #chama a funcao menu pos-login      
                    menu_apos_login(usuario_logado)
            elif op == 2:
                cadastro_usuario() 
            elif op == 0:
                print("Saindo do FeiFood. Até mais!")
                break #sai do loop 'while True' e encerra o programa.
        else:
            print("Opção inválida.")

#inicializando o programa
if __name__ == "__main__":
    menuPrincipal()