""" IMPORTANDO O DB QUE CRIAMOS E A TABELA AGENDAMENTO QUE FOI DEFINIDA NO MODELS.PY"""
from models import db, Agendamento

""" DEFINE UMA FUNÇÃO QUE BUSCA OS AGENDAMENTOS DO BANCO"""
def listar_agendamentos():
    return Agendamento.query.all() #CONSULTA NO BANCO E RETORNA OS REGISTROS DA TABELA

""" FUNCAO QUE RETORNA OS 4 DADOS DEFINIDOS NO FORMULARIO"""
def inserir_agendamento(nome, servico, data, horario):
    novo = Agendamento(nome=nome, servico=servico, data=data, horario=horario)
    db.session.add(novo) #COLOCA AS INFORMAÇÕES NOVAS NA FILA
    db.session.commit() #SALVA NO BANCO
