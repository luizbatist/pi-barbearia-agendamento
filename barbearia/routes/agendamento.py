""" IMPORTANDO AS BIBLIOTECAS"""
from flask import Blueprint, render_template, request, redirect, url_for
""" IMPORTANDO AS FUNCOES QUE CRIAMOS NOS OUTROS ARQUIVOS"""
from database.agendamento import listar_agendamentos, inserir_agendamento

""" CRIA O BLUE PRINT QUE CRIAMOS NO MAIN.PY"""
agendamento_route = Blueprint('agendamento', __name__)

""" DEFINE A ROTA COM DOIS METODOS GET E POST"""
@agendamento_route.route('/', methods=['GET', 'POST'])

def index(): 
    if request.method == 'POST':
        nome = request.form['nome']
        servico = request.form['servico']
        data = request.form['data']
        horario = request.form['horario']
        inserir_agendamento(nome, servico, data, horario)
        return redirect(url_for('agendamento.index'))

    agendamentos = listar_agendamentos()
    return render_template('index.html', agendamentos=agendamentos)

""" FUNCAO QUE SERA EXECUTADA QUANDO O USUARIO ACESSAR A ROTA """