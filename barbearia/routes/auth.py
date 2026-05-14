""" IMPORTANDO AS BIBLIOTECAS """
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.usuario import criar_usuario, buscar_usuario_por_email, verificar_senha

auth_route = Blueprint('auth', __name__)

@auth_route.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """ Rota para criar uma nova conta """
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se o email ja esta cadastrado
        if buscar_usuario_por_email(email):
            flash('Este email já está cadastrado. Faça login.', 'danger')
            return redirect(url_for('auth.cadastro'))

        criar_usuario(nome, email, senha)
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')


@auth_route.route('/login', methods=['GET', 'POST'])
def login():
    """ Rota para entrar na conta """
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = buscar_usuario_por_email(email)

        if usuario and verificar_senha(usuario, senha):
            # Salva os dados do usuario na sessao
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['is_admin'] = usuario.is_admin
            if usuario.is_admin:
                return redirect(url_for('agendamento.admin')) # Manda pro painel do barbeiro
            else:
                return redirect(url_for('agendamento.dashboard')) # Manda pro painel do cliente

        flash('Email ou senha incorretos.', 'danger')

    return render_template('login.html')


@auth_route.route('/logout')
def logout():
    """ Rota para sair da conta """
    session.clear()
    return redirect(url_for('auth.login'))
