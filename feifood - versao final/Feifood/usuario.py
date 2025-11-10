from config import lista_usuarios, espaco

def ler_usuarios(arq_usuario='usuarios.txt'):
    global lista_usuarios
    lista_usuarios.clear()
    try:
        with open(arq_usuario, 'r') as usuarios:
            for linha in usuarios:
                linha = linha.strip()
                if not linha:
                    continue

                dados_usuario = linha.split(',')
                if len(dados_usuario) == 3:
                    usuarios = {
                        'nome': dados_usuario[0].strip(),
                        'e-mail': dados_usuario[1].strip(),
                        'senha':dados_usuario[2].strip()
                    }
                    lista_usuarios.append(usuarios)
    except FileNotFoundError:
        pass
    return lista_usuarios

#função que salva dados do usuario no arquivo 'usuarios.txt'
def salvar_cadastro_usuario():
    try:    #inicia o bloco para executar o cod prevenindo erro
        with open('usuarios.txt', 'w') as usuarios: #abre o arquivo no modo write (sobreescreve o arquivo todo a cada salvamento)
            for usuario in lista_usuarios:  #percorre cada dicionario de usuario na lista_usuarios
                usuarios.write(f"{usuario['nome']},{usuario['e-mail']},{usuario['senha']}\n") #escreve os dados do usuario no arquivo
    except IOError:   #tratamento do caso de não conseguir acessar/criar o arquivo
        print("Erro ao salvar o arquivo de usuários.")

#funcao de cadastro do usuario / criação de novo usuario
def cadastro_usuario(): 
    global lista_usuarios
    print(f"\n|{"Cadastro":^{espaco}}|")

    #recebendo as informaçoes do novo usuario 
    nome = input("Digite seu nome: ").strip()
    email = input("Informe seu e-mail: ").strip()

    #iniciando a validação do e-mail para evitar duplicidade
    email_existe = False        #variável de controle, declarando um valor booleano para verificação, iniciada como Falso
    #verificando a duplicidade o loop percorre cada item do dicionario na lista 'lista_usuarios' com e-mail cadastrado.
    for usuario_existe in lista_usuarios:
        #checa se o e-mail digitado é igual a algum já cadastrado
        if usuario_existe["e-mail"] == email:
            email_existe = True #se durante a validação encontrou o email na lista é sinalizado e paramos o loop
            break #para o loop quando achamos detectamos a duplicidade
    if email_existe:
        #se o email foi encontrado e o valor TRUE foi sinalizado, então e-mail é duplicado e exibe a mensagem
        print("Usuário já possui cadastro. Informe outro e-mail para cadastro.")
        return                  #encerra a funcao e retorna para o menu principal
    
    #se chegamos aqui, o e-mail foi validado como único e então podemos seguir o fluxo
    senha = input("Cadastre uma senha: ").strip()
           
    #inicializando dicionario do novo usuario
    novo_usuario = {
        "nome": nome,
        "e-mail": email,
        "senha": senha
    }
    #adicionando novo usuario a lista inicializada no inicio 
    lista_usuarios.append(novo_usuario)
    salvar_cadastro_usuario()   #chama a funcao para salvar o novo cadastro no arquivo

    print(f"\nCadastro realizado com sucesso!") #mensagem de validação do cadastro

#funcao de login e autenticação do usuario
def login_usuario():
    print(f"\n|{"Login":^{espaco}}|") #imprime o cabeçalho do menu de login centralizado
    usuario = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    #verificação de login o loop inspeciona cada dicionario de usuario na lista
    for login_existente in lista_usuarios:
        #aqui a verificação só é executada se ambas as condições forem verdadeiras
        if login_existente["e-mail"] == usuario and login_existente["senha"] == senha:
            print(f"\nOlá,{login_existente['nome']}!")     #acessando o valor da chave "nome" do dicionario
            return login_existente  #retorna o dicionario do usuario logado (sinal de sucesso)
    print("E-mail ou senha inválidos.") #se o loop terminar e o return não foi chamado, o login falhou
    return None         #não devolve nada ao menu, sinalizando a falha 

#funcao para remover cadastro 
def remover_usuario(usuario_logado):
    global lista_usuarios
    print(f"\n|{'Excluir Conta':^{espaco}}|")
    #confirmacao de exclusao da conta
    validacao = input(f"Tem certeza que deseja EXCLUIR sua conta? 'SIM' para confirmar: ")
    email_excluir = usuario_logado['e-mail'] #armazena o e-mail do usuario logado 
    removido_sucesso = False    #variavel de controle
    #bloco principal 
    if validacao.upper() == 'SIM' or validacao.upper() == 'S':
        #percorre a lista de usuario em busca do dicionario para remover
        for usuario in lista_usuarios:
            if usuario['e-mail'] == email_excluir:  #valida se o usuario logado é o mesmo do usuario no loop
                lista_usuarios.remove(usuario)      #remove o dicionario completo da lista
                removido_sucesso = True
                break
        if removido_sucesso:                        #valida se o loop encontrou e removeu o usuario
            salvar_cadastro_usuario()
            print(f"\nConta de {usuario_logado['nome']} excluída com sucesso! Encerrando seu acesso... ")    
            return True
        else:
            print("Usuario não encontrado")
            return False
    else:
        print("Exclusão não concluída")
        return False
