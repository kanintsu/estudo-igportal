import sqlite3
from flask import Flask, render_template, request, redirect, url_for,session

app = Flask(__name__)
app.secret_key = "neto"

def criar_banco():
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf TEXT NOT NULL UNIQUE,
    data_nascimento TEXT NOT NULL,
    codigo_funcionario TEXT NOT NULL UNIQUE,
    data_admissao TEXT NOT NULL,
    nome TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL)""")

    conexao.commit()
    conexao.close()
criar_banco()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    if request.method == "POST":

        email = request.form["email"]
        cpf = request.form["cpf"]
        data_nascimento = request.form["data_nascimento"]
        codigo_funcionario = request.form["codigo_funcionario"]
        data_admissao = request.form["data_admissao"]
        nome = request.form["nome"]
        senha = request.form["senha"]
        cursor.execute("INSERT INTO usuario (nome, cpf, data_nascimento, codigo_funcionario, data_admissao, email, senha) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, cpf, data_nascimento, codigo_funcionario, data_admissao, email, senha))
        conexao.commit()
        conexao.close()
        return render_template("cadastro.html", mensagem="Cadastro realizado com sucesso!")
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        cursor.execute("SELECT * FROM usuario WHERE email = ? AND senha =  ?", (email, senha,))
    usuario = cursor.fetchone()
    conexao.close()
    if usuario:
        return redirect("/index")
    else:
        return render_template("login.html", mensagem="Email ou senha incorretos!")

app.run(debug=True)