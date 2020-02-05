#aqui, são importadas algumas bibliotecas do peewee 
from peewee import CharField, FloatField, IntegerField, BigBitField, ForeignKeyField, SqliteDatabase, Model
import os #importa o os, usado para remover o arquivo de banco de dados caso ele já exista

arq = "ballot.db" #define o nome do arquivo bd a uma variável
db = SqliteDatabase(arq) #define que o banco vai ser SQLite e qual vai ser o nome do arquivo

class BaseModel(Model): #uma classe que será importada para todas terem acesso ao bd; #Model já existe dentro do próprio peewee
    class Meta: #classe padrão
        database = db #define que o database(banco de dados) é o db

class Usuario(BaseModel): #define a classe Usuario
    nomeU = CharField() #cria a variável nome do tipo CharField( formato usado para palavras )
    cpf = CharField() #cria a variável cpf do tipo CharField( usa-se esse tipo pois no cpf tem pontos e hífen )
    emailU = CharField() #variável email
    senha = CharField() #variável senha
    
class Votacao(BaseModel): #define a classe votação
    titulo = CharField()
    criador = ForeignKeyField(Usuario) #define uma relação entre as classe Votacao e Usuario, o criador vai ser o usuário que criou a votação    
    estiloVotacao = CharField()
    codigo_votacao = CharField()

class Candidato(BaseModel): #define a classe Candidato 
    nomeC = CharField()
    foto = BigBitField(null=False)
    descricao = CharField()
    votacao = ForeignKeyField(Votacao)  #relação entre classes    
    quantidade_votos = IntegerField()

if __name__ == '__main__': #condição verdadeira para garantir que o código seja executado
    if os.path.exists(arq): #entra no if se o arquivo já existir
        os.remove(arq) #exclui arquivo
    db.connect() #conecta no bd
    db.create_tables([Usuario, Candidato, Votacao]) #cria tabelas com base nas classes criadas
    usu = Usuario.create(nomeU='José', cpf='123', emailU='@gmail.com', senha='12345') #instancia objeto
    voto1 = Votacao.create(titulo="Oi", criador=usu.id, estiloVotacao="privada", codigo_votacao="1234")
    vot = Votacao.select() #seleciona todos os valores cadastrados na classe 
    for u in vot:#para cada item da lista vot
        print(u.titulo, u.criador, u.criador.nomeU)#mostra os atributos do item