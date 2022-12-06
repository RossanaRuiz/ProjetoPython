class Cliente:
  def __init__(self, nome, senha, cpf, telefone, email):
    self.nome = nome
    self.senha = senha
    self.cpf = cpf
    self.telefone = telefone
    self.email = email 
    self.idCliente  = -1

  def atribuibId(self, idCliente):
    self.idCliente = idCliente