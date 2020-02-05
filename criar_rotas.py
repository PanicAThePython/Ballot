from flask import Flask, render_template, request, url_for, session, redirect #importa tido que será necessário
from classe import *
from bdballot import *
from random import randint

app = Flask("__name__")#conecta com o Flask
app.config["SECRET_KEY"] = 'admin'#define o usuario
sessao = False #define a sessao como falsa
senha_correta = "" #define a senha
lista_votacoes = Votacao.select() #define a lista de votacoes como tudo que estiver cadastrado na classe Votacao
lista_candidatos = Candidato.select()#define a lista de candidatos como tudo que estiver cadastrado na classe Candidato
vot = ""

@app.route("/")#define a rota
def home():#abre função conectada à rota
    global sessao #define sessao como uma variavel global
    if sessao == True: #se a sessao tiver o valor True, entra no if
        return render_template("index.html", usuario=sessao)#retorn a pagina inicial com o usuario conectado
    else:# se não estiver conectado
        return render_template("index.html", usuario=sessao)#retorn a pagina inicial com o usuario desconectado

@app.route("/form_criar_votacao")#define a rota
def form_criar_votacao():#abre função conectada à rota
    return render_template("criar_votacao.html")#retorna a pagina entre parenteses

@app.route("/form_add_candidato")#define a rota
def add_candidato():#abre função conectada à rota
    session['ncandidatos'] = 2 #define que o numero minimo de candidatos é 2
    return render_template("adicionar_candidatos.html", ncandidatos = session['ncandidatos'])#retorna a pagina entre parenteses acompanhada da lista de candidatos

@app.route("/atualizar_form_add_candidato")#define a rota
def atualizar_form_criar_votacao():#abre função conectada à rota
    return render_template("adicionar_candidatos.html", ncandidatos = session['ncandidatos'])#retorna a pagina entre parenteses acompanhada da lista de candidatos

@app.route("/criar_votacao", methods=['post'])#define a rota com metodo post
def criar_votacao():#abre função conectada à rota
    global senha_correta #define como variavel global
    global vot
    lista_usuarios = Usuario.select() #define lista_usuarios como tido que estiver cadastrado na classe Usuario
    titulo = request.form['titulo'] #pega o valor do form e joga na variavel
    estiloVotacao = request.form['vote'] #pega o valor do form e joga na variavel
    if estiloVotacao == "publ": #se o estilo da votacao for publico, entra no if
        senha_correta = 'u' #define um novo valor pra senha_correta
    elif estiloVotacao == "priv": #se for privada
        gerarSenha()#chama a função
    for i in lista_usuarios:# pra cada item na lista
        if session['usuario'][0] == i.nomeU:#se a primeira posição da sessão for igual ao nome
            idCriador = i.id #define o id do criador igual ao id do usuario
            vot = Votacao.create(titulo=titulo, criador=idCriador, estiloVotacao=estiloVotacao, codigo_votacao=senha_correta)#cria instancia da classe Votacao
    return render_template("eleicao.html", titulo=titulo)#retorna a pagina entre parenteses acompanhada do titulo da votacao

@app.route("/resetar")#define a rota
def resetar():#abre função conectada à rota
    session['ncandidatos'] = 2
    return redirect("/atualizar_form_add_candidato")#redieciona para a rota entre parenteses

@app.route("/salvar_candidatos")#define a rota
def salvarCandidato():#abre função conectada à rota
    global vot
    for t in range(session['ncandidatos']):
        nome = request.args['cand'+str(t+1)]
        desc = request.args['descricao'+str(t+1)]
        c = Candidato.create(nomeC=nome, descricao=desc, votacao=vot, quantidade_votos=0)   
    return 'Deu porra'

@app.route("/votar")#define a rota
def votar():#abre função conectada à rota
    global sessao #define a variavel como global
    return render_template("votar.html", usuario=sessao)#retorna a pagina entre parenteses acompanhada do estado do user: logado ou não

@app.route("/ver_ranking")#define a rota
def ver_ranking():#abre função conectada à rota
    global sessao #define a variavel como global
    return render_template("ver_ranking.html", usuario=sessao)#retorna a pagina entre parenteses acompanhada do estado do user

@app.route("/form_cadastrar")#define a rota
def form_cadastrar():#abre função conectada à rota
    return render_template("cadastrar.html")#retorna a pagina entre parenteses

@app.route("/cadastrar", methods=['post'])#define a rota com metodo post
def cadastrar():#abre função conectada à rota
    nomeU = request.form['nome']#pega o valor do form e joga na variavel
    cpf = request.form['cpf']#pega o valor do form e joga na variavel
    emailU = request.form['email']#pega o valor do form e joga na variavel
    senha = request.form['senha']#pega o valor do form e joga na variavel
    Usuario.create(nomeU=nomeU, cpf=cpf, emailU=emailU, senha=senha)#cria instancia da classe Usuario
    #Colocar alert informando que foi bem sucedido! E o verificador se os campos estiverem preenchidos!
    return redirect("/form_login")#redireciona para a rota entre parenteses

@app.route("/form_login")#define a rota
def form_login():#abre função conectada à rota
    return render_template("form_login.html")#retorna a pagina entre parenteses

@app.route("/login", methods=['post'])#define a rota com metodo post
def login():#abre função conectada à rota
    global sessao#define a variavel como global
    lista_usuarios = Usuario.select()#define lista_usuarios como tido que estiver cadastrado na classe Usuario
    emailU = ',1' #define a variavel
    senhadigitada = request.form['senha']#pega o valor do form e joga na variavel
    emailUdigitado = request.form['email']#pega o valor do form e joga na variavel

    for procura in lista_usuarios:#pra cada item na lista
        if emailUdigitado == procura.emailU:#se o email digitado por igual ao email 
            emailU = procura.emailU #define email
            senha = procura.senha #define senha
    
    if emailUdigitado == emailU and senha == senhadigitada:#se o email e a senha forem iguais ao os valores guaradados
        sessao_total = (emailU, senha)#a sessao total é igual ao email e a senha do user
        session['usuario'] = sessao_total #a sessao do user é igual a sessao total
        sessao = True #sessao vale True
        return render_template("index.html")#retorna a pagina entre parenteses
    else:#se não forem iguais
        #Colocar alert e voltar pra tela de login
        #Ainda tem erros com mais de  1 cadastro
        return redirect("/form_login")#redireciona para a rota entre parenteses

@app.route("/logout")#define a rota
def logout():#abre função conectada à rota
    global sessao#define a variavel como global
    sessao = False#sessao vale False
    session.pop('usuario')#remove o usuario da sessao
    return redirect("/")#redireciona para a rota entre parenteses

@app.route("/soma")#define a rota
def soma():#abre função conectada à rota
    session['ncandidatos'] += 1#adiciona mais um candidato na tela
    return redirect("/atualizar_form_add_candidato")#redireciona à rota entre parenteses

def gerarSenha():#abre função 
    global senha_correta#define a variavel como global
    senha = []#senha é uma lista vazia
    contador = 0#contador vale zero
    if senha_correta == '':#se a senha for igual à padrao
        while 10 > len(senha):#enqunto o tamanho da senha for menor que 10
            aleatorio = randint(36,165)#pega um numero aleatorio entre 36 e 164 e joga na variavel
            algarismo = chr(aleatorio)#define a variavel como igual ao caracter correspondente ao numero dentro de aleatorio
            senha.append(algarismo)#adiciona o algarismo na lista senha
        while contador < len(senha):#enquanto o tamanho da senha for maior que o contador
            senha_correta += str(senha[contador])#senha_correta é igual a ela mesma mais cada item da lista ate acabar a condição
            contador += 1 #contador vale ele mesmo mais um
        print("SENHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")#mostra o que está entre parenteses
        print(senha_correta)#mostra o que está entre parenteses
    return True #retorna True

@app.route("/pagina_votacao", methods=['POST'])#define a rota com metodo post
def paginaVotacao():#abre função conectada à rota
    codV = request.form["codV"]#pega o valor do form e joga na variavel
    try:#tentar
        for i in lista_votacoes:#para cada item dentro da lista
            if codV == lista_votacoes.codigo_votacao:#se a variavel for igual ao codigo da votacao dentro da lista
                return redirect("/")#redireciona à rota entre parenteses
            else:#se não for igual 
                return 'Algo deu errado!'#retorna que algo deu errado
    except:#se não der certo
        return "alert('O codigo nao existe')" #alerta que o codigo não existe
    return "<script>alert('Algo Errado')</script>\
            <a href='/votar'>Voltar</a>"  #retorna um comando javascript e um link html

@app.route("/voltar")#define a rota
def voltar():#abre função conectada à rota
    return redirect("/")#redireciona à rota entre parenteses

app.run(debug=True, port=7500, host="0.0.0.0")#manda o servidor rodar, na porta 7500, no host 0.0.0.0 e aceita qualquer mudança feita durante seu funcionamento