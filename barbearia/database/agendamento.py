""" IMPORTANDO AS BIBLIOTECAS """
from models import db, Agendamento, Usuario

def inserir_agendamento(usuario_id, servico, data, horario):
    """ Insere um novo agendamento ligado ao usuario """
    agendamento = Agendamento(
        usuario_id=usuario_id,
        servico=servico,
        data=data,
        horario=horario,
        status='Agendado'
    )
    db.session.add(agendamento)
    db.session.commit()

def horario_disponivel(data, horario):
    """ Verifica se o horario ja esta ocupado por um agendamento ativo """
    agendamento_ocupado = Agendamento.query.filter(
        Agendamento.data == data,
        Agendamento.horario == horario,
        Agendamento.status != 'Cancelado'
    ).first()

    return agendamento_ocupado is None  # True se livre, False se ocupado

def atualizar_status_agendamento(agendamento_id, novo_status, usuario_id=None):
    agendamento = db.session.get(Agendamento, agendamento_id)

    if not agendamento:
        return False

    if usuario_id is not None and agendamento.usuario_id != usuario_id:
        return False # Tentativa de cancelar agendamento de outra pessoa

    agendamento.status = novo_status
    db.session.commit()
    return True

def listar_agendamentos_por_usuario(usuario_id):
    """ Retorna apenas os agendamentos do usuario logado """
    return Agendamento.query.filter_by(usuario_id=usuario_id).all()

def listar_todos_agendamentos():
    """ Retorna todos os agendamentos (somente para admin) """
    return Agendamento.query.join(Usuario).all()

def buscar_horarios_ocupados_por_data(data):
    """ Retorna uma lista com os horários que já estão ocupados em uma data específica """
    ocupados = Agendamento.query.filter(
        Agendamento.data == data,
        Agendamento.status != 'Cancelado'
    ).all()

    return [agendamento.horario for agendamento in ocupados]