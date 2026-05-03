""" IMPORTANDO AS BIBLIOTECAS """
from models import db, Agendamento, Usuario

def inserir_agendamento(usuario_id, servico, data, horario):
    """ Insere um novo agendamento ligado ao usuario """
    agendamento = Agendamento(
        usuario_id=usuario_id,
        servico=servico,
        data=data,
        horario=horario
    )
    db.session.add(agendamento)
    db.session.commit()

def horario_disponivel(data, horario):
    """ Verifica se o horario ja esta ocupado """
    agendamento = Agendamento.query.filter_by(data=data, horario=horario).first()
    return agendamento is None  # True se disponivel, False se ocupado

def listar_agendamentos_por_usuario(usuario_id):
    """ Retorna apenas os agendamentos do usuario logado """
    return Agendamento.query.filter_by(usuario_id=usuario_id).all()

def listar_todos_agendamentos():
    """ Retorna todos os agendamentos (somente para admin) """
    return Agendamento.query.join(Usuario).all()