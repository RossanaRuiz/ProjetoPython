import sqlite3
from sqlite3 import Error


class Criacao:

  def __init__(self):
    pass

  def criaClientes(self):
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS clientes (
        idCliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        cpf VARCHAR(11) NOT NULL UNIQUE,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL
      );
      """)
    conn.close()

  def criarTabela(self):
    conn = sqlite3.connect('laboratorio.db')
    cursor = conn.cursor()
    try:
      print("1")
      '''
      cursor.execute("""
      CREATE TABLE IF NOT EXISTS clientes (
        idCliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        cpf VARCHAR(11) NOT NULL UNIQUE,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL
      );
      
      """)
      print("2")
      cursor.execute("""
      CREATE TABLE IF NOT EXISTS salas(
          idsala INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          nome TEXT NOT NULL,
          numero INT NOLL NULL,
          capacidade INT NOT NULL
      );
        """)
      print("3")
      cursor.execute("""
      CREATE TABLE IF NOT EXISTS alugar(
          id INTEGER  NOT NULL  PRIMARY KEY AUTOINCREMENT,
          codigo TEXT NOT NULL,
          data TEXT NOT NULL,
          cpfCliente VARCHAR(11)  NOT NULL,
          idCliente INTERGER NOT NULL,
          idSala INTERGER NOT NULL,
          CONSTRAINT fk_cliente FOREIGN KEY (idCliente) REFERENCES clientes (idcliente)
          CONSTRAINT fk_salas FOREIGN KEY (idsala) REFERENCES salas (idSala)
      );
      """)

      print("4")

      cur = conn.cursor()
      cur.execute("""
          INSERT INTO salas (nome,numero,capacidade) VALUES 
              ('Laboratorio de Informatica',401, 20),
              ('Laboratorio de Quimica', 402, 15),
              ('Laboratorio de Fisica',403, 15),
              ('Laboratorio de Informatica',404, 30),
              ('Laboratorio de Astronomia',405, 20),
              ('Laboratorio de Quimica',406, 03),
              ('Laboratorio de Informatica', 407, 35);
            
            """)
      conn.close()
      print("5")
      '''
      connee = sqlite3.connect('laboratorio.db')
      cursorr = connee.cursor()
      cursorr.execute(""" SELECT * FROM salas;""")
      for linha in cursorr.fetchall():
        print(linha)
      conn.close()
      print("6")

    except Error as e:
      print(e)
