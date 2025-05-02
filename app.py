from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'biblioteca123'

USUARIOS_FILE = 'usuarios.json'
LIVROS_FILE = 'livros.json'
EMPRESTIMOS_FILE = 'emprestimos.json'
RESERVAS_FILE = 'reservas.json'

matriculas_validas = ["aluno001", "aluno002", "aluno003"]

# Funções utilitárias para JSON
def carregar_json(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_json(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def efetuar_login():
    nome = request.form['nome']
    senha = request.form['senha']
    usuarios = carregar_json(USUARIOS_FILE)
    for u in usuarios:
        if u['nome'] == nome and u['senha'] == senha:
            session['usuario'] = nome
            session['tipo'] = u['tipo']
            flash('Login realizado com sucesso!', 'success')
            if u['tipo'] == 'bibliotecario':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('aluno'))
    flash('Usuário ou senha inválidos.', 'error')
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        matricula = request.form['matricula']
        usuarios = carregar_json(USUARIOS_FILE)

        if any(u['nome'] == nome for u in usuarios):
            flash('Usuário já existe.', 'error')
            return redirect(url_for('cadastro'))

        if matricula not in matriculas_validas:
            flash('Matrícula inválida.', 'error')
            return redirect(url_for('cadastro'))

        usuarios.append({"nome": nome, "senha": senha, "tipo": "aluno"})
        salvar_json(USUARIOS_FILE, usuarios)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session or session['tipo'] != 'bibliotecario':
        return redirect(url_for('login'))
    emprestimos = carregar_json(EMPRESTIMOS_FILE)
    reservas = carregar_json(RESERVAS_FILE)
    return render_template('dashboard.html', usuario=session['usuario'], emprestimos=emprestimos, reservas=reservas)

@app.route('/aluno', methods=['GET', 'POST'])
def aluno():
    if 'usuario' not in session or session['tipo'] != 'aluno':
        return redirect(url_for('login'))

    if request.method == 'POST':
        codigo = request.form['codigo']
        reservas = carregar_json(RESERVAS_FILE)
        reservas.append({
            'aluno': session['usuario'],
            'codigo': codigo,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M')
        })
        salvar_json(RESERVAS_FILE, reservas)
        flash('Livro reservado com sucesso!', 'success')
        return redirect(url_for('aluno'))

    livros = carregar_json(LIVROS_FILE)
    return render_template('aluno.html', usuario=session['usuario'], livros=livros)

@app.route('/cadastrar_livro', methods=['GET', 'POST'])
def cadastrar_livro():
    if 'usuario' not in session or session['tipo'] != 'bibliotecario':
        return redirect(url_for('login'))

    if request.method == 'POST':
        livros = carregar_json(LIVROS_FILE)
        titulo = request.form['titulo']
        autor = request.form['autor']
        genero = request.form['genero']
        codigo = request.form['codigo']
        livros.append({
            'titulo': titulo,
            'autor': autor,
            'genero': genero,
            'codigo': codigo,
            'disponivel': True
        })
        salvar_json(LIVROS_FILE, livros)
        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('cadastrar_livro.html')

@app.route('/buscar')
def buscar():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    livros = carregar_json(LIVROS_FILE)
    return render_template('buscar.html', livros=livros)

@app.route('/emprestar', methods=['GET', 'POST'])
def emprestar():
    if 'usuario' not in session or session['tipo'] != 'bibliotecario':
        return redirect(url_for('login'))

    livros = carregar_json(LIVROS_FILE)
    emprestimos = carregar_json(EMPRESTIMOS_FILE)
    reservas = carregar_json(RESERVAS_FILE)

    if request.method == 'POST':
        aluno = request.form['aluno']
        codigo = request.form['codigo']

        for livro in livros:
            if livro['codigo'] == codigo and livro['disponivel']:
                livro['disponivel'] = False
                data_emprestimo = datetime.now()
                previsao_devolucao = data_emprestimo + timedelta(days=7)
                emprestimos.append({
                    'aluno': aluno,
                    'codigo': codigo,
                    'data': data_emprestimo.strftime('%d/%m/%Y'),
                    'previsao': previsao_devolucao.strftime('%d/%m/%Y')
                })
                reservas = [r for r in reservas if not (r['aluno'] == aluno and r['codigo'] == codigo)]
                break

        salvar_json(LIVROS_FILE, livros)
        salvar_json(EMPRESTIMOS_FILE, emprestimos)
        salvar_json(RESERVAS_FILE, reservas)
        flash('Empréstimo registrado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('emprestar.html', livros=livros)

@app.route('/devolver', methods=['POST'])
def devolver():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    codigo = request.form['codigo']
    livros = carregar_json(LIVROS_FILE)
    emprestimos = carregar_json(EMPRESTIMOS_FILE)

    for livro in livros:
        if livro['codigo'] == codigo:
            livro['disponivel'] = True
            break

    emprestimos = [e for e in emprestimos if e['codigo'] != codigo]

    salvar_json(LIVROS_FILE, livros)
    salvar_json(EMPRESTIMOS_FILE, emprestimos)
    flash('Livro devolvido com sucesso!', 'success')
    return redirect(url_for('buscar'))

@app.route('/exportar/<arquivo>')
def exportar(arquivo):
    caminho = f"{arquivo}.json"
    if os.path.exists(caminho):
        return send_file(caminho, as_attachment=True)
    return "Arquivo não encontrado", 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
