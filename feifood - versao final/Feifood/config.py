lista_usuarios = []
lista_pedidos = []
espaco = 100  
prox_id_pedido = 1

#menu da entrada / #dicionario que armazena as opções do menu principal (utilizado chave:valor - para facilitar a checagem)
opcoes = {
    1 : "Login",
    2 : "Cadastro",
    0 : "Sair"
}

#opcoes de navegacao apos o login do usuario
opcoes_usuario = {
    1 : "Buscar por alimento",
    2 : "Cadastrar pedido",
    3 : "Gerenciar pedidos",
    4 : "Avaliar pedido",
    5 : "Excluir Conta",
    0 : "Sair"
}

#dicionario com as opções de gerenciamento de pedidos após login
opcao_gerenc_pedido ={
    1: "Editar",
    2: "Excluir",
    0: "Voltar"

}
