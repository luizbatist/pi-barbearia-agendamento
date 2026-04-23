""" IMPORTANDO AS BIBLIOTECAS"""
from flask import Blueprint, render_template, request, redirect, url_for
""" IMPORTANDO AS FUNCOES QUE CRIAMOS NOS OUTROS ARQUIVOS"""
from database.agendamento import listar_agendamentos, inserir_agendamento

""" CRIA O BLUE PRINT QUE CRIAMOS NO MAIN.PY"""
agendamento_route = Blueprint('agendamento', __name__)

@agendamento_route.route('/')
def home():
    """ Rota para a Landing Page (Apresentação) """
    return render_template('index.html')


@agendamento_route.route('/agendar', methods=['GET', 'POST'])
def agendar():
    """ Rota para o sistema de agendamento (Formulário e Lista) """
    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.form['nome']
        servico = request.form['servico']
        data = request.form['data']
        horario = request.form['horario']

        # Insere no banco de dados
        inserir_agendamento(nome, servico, data, horario)

        # Redireciona para a mesma página (limpa o formulário e evita duplicados no F5)
        return redirect(url_for('agendamento.agendar'))

    # Se for GET, busca os agendamentos e renderiza o novo template
    agendamentos = listar_agendamentos()
    return render_template('agendamento.html', agendamentos=agendamentos)

""" FUNCAO QUE SERA EXECUTADA QUANDO O USUARIO ACESSAR A ROTA """