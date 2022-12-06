from clientes import Cliente
from sala import Sala
from alugar import Alugar
import sqlite3
from cores import Cores
from sqlite3 import Error


class Conexao:

  def __init__(self):
    pass

  # retornar todas as salas
  def retornarSalas(self, salas):
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    try:
      cursor.execute(""" SELECT * FROM salas;""")
      for linha in cursor.fetchall():
        s = Sala(linha[0], linha[1], linha[2], linha[3])
        salas.append(s)
      conn.close()
    except Error as e:
      print(e)
    #Retorna id da sala e conta quantidade de reservas de cada sala
  def salasGrafico(self):
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    labels = []
    valores = []
    try:
      cursor.execute(
        """ SELECT salas.idsala,salas.nome, count(alugar.id) FROM salas LEFT JOIN alugar ON alugar.idsala = salas.idsala Group By salas.idsala"""
      )
      for linha in cursor.fetchall():
        labels.append(str(linha[0]))
        valores.append(linha[2])
      conn.close()
    except Error as e:
      print(e)
    return {'labels': labels, 'valores': valores}

  # cadastrar cliente
  def salvar(self, cliente):
    t = (cliente.nome, cliente.senha, cliente.cpf, cliente.telefone,
         cliente.email)

    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    try:
      cursor.execute(
        """
        INSERT INTO clientes(nome, senha, cpf, telefone, email) VALUES (?,?,?,?,?)
      """, t)
      conn.commit()
      conn.close()
      
    except Error as e:
      print(e)

  # excluir cliente por cpf
  def excluirPorCpf(self, cpf):
    t = (cpf)
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    try:
      cursor.execute(
        """
        DELETE FROM clientes where cpf = ?
        """, t)
      conn.commit()
      conn.close()
    except Error as e:
      print(e)

  # inserir alugar na tabela de salas
  #def alugar(self, codigo, data, cpf):
  def alugar(self, codigo, data, cpf, idCliente):
    connAlugar = sqlite3.connect('laboratorio.db')
    cursorAlugar = connAlugar.cursor()
    try:
      t = (data, cpf, idCliente, codigo)
      cursorAlugar.execute(
        """
        INSERT INTO  alugar (data, cpfCliente,idCliente, idSala) VALUES (?,?,?,?)
      """, t)
      connAlugar.commit()
      connAlugar.close()
    except Error as e:
      print(e)

  # logar no sistema
  def logar(self, cliente):
    t = (str(cliente[0]), str(cliente[1]))
    conn = sqlite3.connect('laboratorio.db')
    cur = conn.cursor()
    try:
      cur.execute("SELECT * FROM clientes WHERE nome = ? AND senha = ?", t)

      status = -1
      rows = cur.fetchall()
      if len(rows) == 1:
        cliente = rows[0]
        clienteRetorno = Cliente(cliente[1], cliente[2], cliente[3],
                                 cliente[4], cliente[5])
        # Função de atribuição do id, indicando que o cliente ja esta salvo no banco
        clienteRetorno.atribuibId(cliente[0])
        
        status = 1
      else:
        clienteRetorno = ''
        print(f'{Cores.BOLD}{Cores.FAIL}Usuario invalido!!{Cores.ENDC}')
      conn.close()
      return [status, clienteRetorno]
    except Error as e:
      print(e)

  # mostrar reservas por cpf do cliente
  def minhasReservas(self, cpf):
      connMinhasReservas = sqlite3.connect('laboratorio.db')
      curMinhasReservas = connMinhasReservas.cursor()
      try:
        curMinhasReservas.execute(""" SELECT alugar.id, salas.idsala,salas.nome, alugar.data FROM salas INNER JOIN alugar ON salas.idsala=alugar.idsala WHERE cpfCliente=?; """,(cpf,))
        rows = curMinhasReservas.fetchall()
        if len(rows) > 0:
          for linha in rows:
            #a = Alugar(linha[0], linha[1], linha[2])
            #alugar.append(a)
            print(23 * f'{Cores.BOLD}{Cores.WARNING}={Cores.ENDC}')
            print('[ID da Reserva]:' + str(linha[0]))
            print('Codigo da Sala:' + str(linha[1]))
            print('Nome da Sala: ' + str(linha[2]))
            print('Data da reserva: ' + str(linha[3]))
            print('')
        else:
          print(f'{Cores.BOLD}{Cores.WARNING} Não existem reservas para esse cliente!!{Cores.ENDC}')
        connMinhasReservas.close()
      except Error as e:
        print(e)

 # excluir uma reserva baseada no id assume-se que a pessoa ja viu os ids das reservas
  def excluirReservaPorId(self, id, cpfCliente):
    t = (id,cpfCliente)
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    try:
      # coloquei cpf como parametro para impedir que o cliente exclua uma reserva que não é dele
      cursor.execute("""
        DELETE FROM alugar where id = ? AND cpfCliente = ?
        """, t)
      conn.commit()
      conn.close()
      print('Reserva cancelada com sucesso!!')
    except Error as e:
      print(e)
