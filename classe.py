class Usuario(): #define classe Usuario

    def __init__(self, nome, cpf, email, senha): #def __init__ usado para criar os atributos da classe
        self.nome  = nome #cria o atributo nome
        self.cpf   = cpf
        self.email = email
        self.senha = senha