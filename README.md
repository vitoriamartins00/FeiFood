# FEIFood: Plataforma de pedidos

O Porjeto FEIFood consiste em uma plataforma de gerenciamento de pedidos de alimentos, desenvolvida em Python para a disciplina de Fund. de Algoritmos. O projeto simula o fluxo completo de um app de delivery, desde o cadastro até a avaliação e persistência dos dados em arquivos de texto.

# Func. Principais

O sistema foi modularizado para organizar as responsabilidades (Usuário, Pedido e Cardápio), implementando o gerenciamento completo da conta do usuário e pedidos.

1. Gestão de Usuário (mód. usuario.py)
   -  Cadastro: Criação de novos usuários com a validação de duplicidade de e-mail
   -  Login: Autenticação por e-mail e senha
   -  Exclusão de Conta: Permite que o usuário logado remova sua conta do sistema
     
2. Gestão de Pedidos(mód. pedidos.py)
   - Criação: Permite criar um novo pedido, selecionando itens do cardápio
   - Edição (CRUD): Permite adicionar ou remover itens de um pedido existente e recalcula o valor total
   - Exclusao: Remove um pedido da lista global e do histórico
   - Avaliação: Permite que o usuário atribua uma nota (de 0 a 5) a um pedido já finalizado
     
3. Cardápio e Busca (mód. cardapio.py)
   - Visualização: Exibe o cardápio completo de alimentos com preços e descrição
   - Busca: Permite buscar alimentos por palavras-chave no nome
  
4. Persistência de Dados (Armazenamento)
   - Todos os dados de cadastro, criação e ou alterações são salvos em arquivos de texto simples, garantindo a persistência dos dados das sessões
     - usuarios.txt: Armazena os dados dos clientes
     - pedidos.txt: Armazena o histórico completo de transações


# Para execução do Projeto
Para rodar o projeto em seu ambiente local, siga os passos abaixo;

Passo 1: Instale python 3.12

Passo 2: Clone o repositório: 
git clone https://github.com/vitoriamartins00/FeiFood.git

Passo 3: Certifique-se de que todos os arquivos .py (main.py, usuario.py, pedidos.py, cardapio.py, config.py) e os arquivos de dados vazios (usuarios.txt, pedidos.txt) estejam na mesma pasta

Passo 4: Execute o programa:
python main.py


# Estrutura do Projeto

O projeto segue uma arquitetura modular, onde cada arquivo é responsável por um domínio específico:

-main.py: Controla o fluxo de navegação e inicializa o programa
-config.py: Armazena variáveis globais, listas de dados e constantes de menu
-usuario.py: Gerencia o ciclo de vida do usuário (cadastro, login e exclusão)
-pedidos.py: Gerencia todas as transações, manipulação e persistência  dos pedidos
-cardapio.py: Define a lista de alimentos disponíveis e lógica de busca


# Autor

Este projeto foi desenvolvido por:
Vitoria Carolyne Martins Souza - RA 742250038
