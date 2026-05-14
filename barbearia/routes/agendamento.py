""" IMPORTANDO AS BIBLIOTECAS """
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from database.agendamento import inserir_agendamento, listar_agendamentos_por_usuario, listar_todos_agendamentos, horario_disponivel,atualizar_status_agendamento,buscar_horarios_ocupados_por_data

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
    if session.get('is_admin'):
        return redirect(url_for('agendamento.admin'))
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

@agendamento_route.route('/agendamento/<int:id>/status', methods=['POST'])
@login_required
def alterar_status_admin(id):
    """ Rota exclusiva para o barbeiro Concluir ou Cancelar um agendamento """
    if not session.get('is_admin'):
        flash('Acesso restrito.', 'danger')
        return redirect(url_for('agendamento.dashboard'))

    novo_status = request.form.get('novo_status')

    if novo_status in ['Concluído', 'Cancelado']:
        atualizar_status_agendamento(id, novo_status)
        flash(f'Agendamento {novo_status.lower()} com sucesso!', 'success')
    else:
        flash('Status inválido.', 'danger')

    return redirect(url_for('agendamento.admin'))


@agendamento_route.route('/agendamento/<int:id>/cancelar_cliente', methods=['POST'])
@login_required
def cancelar_cliente(id):
    usuario_logado = session['usuario_id']
    sucesso = atualizar_status_agendamento(id, 'Cancelado', usuario_logado)
    if sucesso:
        flash('Agendamento cancelado com sucesso. O horário já está livre na agenda.', 'success')
    else:
        flash('Erro: Você não tem permissão para cancelar este agendamento ou ele não existe.', 'danger')
    return redirect(url_for('agendamento.meus_agendamentos'))

@agendamento_route.route('/api/horarios-disponiveis')
@login_required
def api_horarios_disponiveis():
    """ API chamada via Javascript para retornar os horários livres de uma data """
    data_escolhida = request.args.get('data')

    if not data_escolhida:
        return jsonify({"erro": "Data não fornecida"}), 400

    horarios_funcionamento = [
        "09:00", "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"
    ]

    horarios_ocupados = buscar_horarios_ocupados_por_data(data_escolhida)

    horarios_livres = [h for h in horarios_funcionamento if h not in horarios_ocupados]

    return jsonify(horarios_livres)