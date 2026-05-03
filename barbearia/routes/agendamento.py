""" IMPORTANDO AS BIBLIOTECAS """
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.agendamento import inserir_agendamento, listar_agendamentos_por_usuario, listar_todos_agendamentos, horario_disponivel

agendamento_route = Blueprint('agendamento', __name__)

""" DECORATOR: bloqueia rotas para quem nao esta logado """
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Faça login para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@agendamento_route.route('/')
def home():
    """ Rota para a Landing Page """
    return render_template('index.html')


@agendamento_route.route('/dashboard')
@login_required
def dashboard():
    """ Pagina principal apos o login com os dois botoes """
    return render_template('dashboard.html')


@agendamento_route.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    """ Rota para fazer um novo agendamento """
    if request.method == 'POST':
        usuario_id = session['usuario_id']
        servico = request.form['servico']
        data = request.form['data']
        horario = request.form['horario']

        if not horario_disponivel(data, horario):
            flash('Este horário já está ocupado. Escolha outro.', 'danger')
            return redirect(url_for('agendamento.agendar'))

        inserir_agendamento(usuario_id, servico, data, horario)
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('agendamento.meus_agendamentos'))

    return render_template('agendamento.html')


@agendamento_route.route('/meus-agendamentos')
@login_required
def meus_agendamentos():
    """ Rota para o cliente ver apenas os proprios agendamentos """
    agendamentos = listar_agendamentos_por_usuario(session['usuario_id'])
    return render_template('meus_agendamentos.html', agendamentos=agendamentos)


@agendamento_route.route('/admin')
@login_required
def admin():
    """ Rota exclusiva para o barbeiro/admin ver todos os agendamentos """
    if not session.get('is_admin'):
        flash('Acesso restrito.', 'danger')
        return redirect(url_for('agendamento.dashboard'))

    agendamentos = listar_todos_agendamentos()
    return render_template('admin.html', agendamentos=agendamentos)