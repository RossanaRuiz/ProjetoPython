from clientes import Cliente
from banco import Conexao
from criacao import Criacao
import os
from os import system
from sqlite3 import Error
from cores import Cores
import matplotlib.pyplot as plt


class Pedido:

  def __init__(self):
    self.conexao = Conexao()
    self.criacao = Criacao()

    #self.conexao.minhasReservas('23766480847')
    #self.criacao.criarTabela()
    self.clientes = []
    self.salas = []
    self.aluguel = []
    self.atuaCliente = None
    self.conexao.retornarSalas(self.salas)



#procura o nome do Sistema Operacional, faz a comparação e ejecuta
  def limpar(self):
    if os.name == "posix":
      system("clear") #linux
    else:
      system("cls") #windows
      
#recebe o nome e senha do cliente procura ele no banco e guarda os seus dados numa tupla
  def logar(self):
    nome = input("Digite o nome: ").title()
    senha = input("Digite a senha: ")
    self.limpar()
    c = (nome, senha)
    resposta = self.conexao.logar(c)
    self.atuaCliente = resposta[1]
    return resposta[0]
    
#recebe os dados do novo cliente e guarda no banco na tabela clientes
  def cadastrar(self):
    nome = input(f"{Cores.BOLD}Digite o nome: ").title()
    senha = input("Digite a senha: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    email = input(f"Email: {Cores.ENDC}")
    c = Cliente(nome, senha, cpf, telefone, email)
    self.clientes.append(c)
    self.conexao.salvar(c)
    print(f"{Cores.BOLD}{Cores.WARNING}Cliente cadastrado com sucesso!!{Cores.ENDC}")
    print(" ")
    
#retorna as salas da tabela "alugar" porem so as que correspondem ao clienteAtual
  def minhasReservas(self):
    cpf = self.atuaCliente.cpf
    self.conexao.minhasReservas(cpf)
    self.excluirReservas()
    
#retorna todas as salas e seus aributos da tabela "salas"
  def mostrarSalas(self):
    for sala in self.salas:
      print('[' + str(sala.id) + '] - ' + sala.nome)
      print('Numero:' + str(sala.numero))
      print('Capacidade:' + str(sala.capacidade) + 'Pessoas')
      print('')
    print('')
    self.alugar()
    
#remove o cliente da tabela "clientes"
  def remover(self):
    nome = input('Digite o nome: ')
    senha = input('Digite a senha: ')
    del (self.clientes)

#chama o grafico q exibe o id das salas e a quantidade de reservas  
  def grafico(self):
    retorno = self.conexao.salasGrafico()
    l = retorno['labels']
    v = retorno['valores']
    fix, ax = plt.subplots(figsize=(8, 5))
    ax.bar(l, v)
    ax.set_title('Reserva de Laboratorios', fontsize=14)
    ax.set_ylabel('Quantidade Reservas', fontsize=12)
    ax.set_xlabel('Id Salas', fontsize=12)
    fig = plt.figure()

    def msg(event):
      self.opcoesReservas()

    fig.canvas.mpl_connect('close_event', msg)
    plt.show()

  def on_close(self):
    print('Closed Figure!')
    
#opção de cancelar uma reserva inserindo o id da reserva
  def excluirReservas(self):
    print(
      f'{Cores.BOLD}{Cores.WARNING}Deseja excluir alguma reserva?{Cores.ENDC}')
    print(f'{Cores.BOLD}[1] - Sim{Cores.ENDC}')
    print(f'{Cores.BOLD}[2] - Não{Cores.ENDC}')
    resp = input(
      f'{Cores.BOLD}{Cores.WARNING}Escreva sua resposta: {Cores.ENDC}')
    if resp == '1':
      id = input('Digite o ID da reserva: ')
      cpfCliente = self.atuaCliente.cpf
      self.conexao.excluirReservaPorId(id, cpfCliente)
      self.minhasReservas()
      
#função exibida depois da funçaõ "MostrarSalas" 
  def alugar(self):
    print(f'{Cores.BOLD}{Cores.WARNING}Deseja alugar alguma sala?{Cores.ENDC}')
    print(f'{Cores.BOLD}[1] - Sim{Cores.ENDC}')
    print(f'{Cores.BOLD}[2] - Não{Cores.ENDC}')
    resp = input(
      f'{Cores.BOLD}{Cores.WARNING}Escreva sua resposta:{Cores.ENDC}')
    if resp == '1':
      codigo = input(
        f'{Cores.BOLD}{Cores.WARNING}Digite o codigo da sala: {Cores.ENDC}')
      d = input(f"{Cores.BOLD}Informe o dia:{Cores.ENDC}")
      m = input(f"{Cores.BOLD}Informe o mes:{Cores.ENDC}")
      a = input(f"{Cores.BOLD}Informe o ano:{Cores.ENDC}")
      data = a + "-" + m + "-" + d
      #cpf = input('Digite seu CPF: ')
      #  self.conexao.alugar(codigo, data, cpf)
      cpf = self.atuaCliente.cpf
      idCliente = self.atuaCliente.idCliente
      self.conexao.alugar(codigo, data, cpf, idCliente)
      print(
        f"{Cores.BOLD}{Cores.WARNING}Reserva realizada com sucesso!!{Cores.ENDC}"
      )
#1ro menu
  def main(self):
    while True:
      op = 0
      while op != '3':
        print(23 * f'{Cores.BOLD}{Cores.WARNING}={Cores.ENDC}')
        print(f"{Cores.BOLD}{Cores.WARNING}     LABORATORIO {Cores.ENDC}")
        print(23 * f'{Cores.BOLD}{Cores.WARNING}={Cores.ENDC}')
        print(f"{Cores.BOLD}Escolha uma opção:")
        print('[1] - Logar')
        print('[2] - Cadastrar')
        print(f"[3] - Sair {Cores.ENDC}")
        op = input(
          f'{Cores.BOLD}{Cores.WARNING}Digite um numero: {Cores.ENDC}')
        self.limpar()

        if op == '1':
          status = self.logar()
          if status == 1:
            self.opcoesReservas()
        elif op == '2':
          self.cadastrar()
        elif op == '3':
          print(f'{Cores.BOLD}{Cores.WARNING}Obrigado por utilizar o sistema!{Cores.ENDC}')
          exit()
        else:
          print('Numero invalido!!')
#2do menu
  def opcoesReservas(self):
    i = 0
    n = self.atuaCliente.nome.upper()
    while i != '5':
      print(23 * f'{Cores.BOLD}{Cores.WARNING}={Cores.ENDC}')
      print(f"{Cores.BOLD}{Cores.WARNING}    BEM-VINDO/A " + n +
            f"   {Cores.ENDC}")
      print(23 * f'{Cores.BOLD}{Cores.WARNING}={Cores.ENDC}')
      print(f'{Cores.BOLD}[1] - Minhas reservas ')
      print('[2] - Mostrar salas ')
      print('[3] - Excluir Usuario')
      print('[4] - Salas mais alugadas')
      print(f'[5] - Sair{Cores.ENDC}')
      i = input(f'{Cores.BOLD}{Cores.WARNING}Digite um numero: {Cores.ENDC}')
      if i == '1':
        self.minhasReservas()
      elif i == '2':
        self.mostrarSalas()
      elif i == '3':
        self.remover()
      elif i == '4':
        self.grafico()
      elif i == '5':
        print('Obrigado por utilizar o sistema.')
      else:
        print(f'{Cores.BOLD}{Cores.FAIL}Numero invalido!!{Cores.ENDC}')

      print(' ')
      print(' ')
