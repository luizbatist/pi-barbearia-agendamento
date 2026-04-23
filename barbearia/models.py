""" IMPORTANDO AS BIBLIOTECAS"""
from flask_sqlalchemy import SQLAlchemy

""" CRIA A VARIAVEL DB QUE VAI SER USADA NO MAIN.PY"""
db = SQLAlchemy()

""" CRIA A TABELA DE AGENDAMENTO"""
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True) #CRIANDO COLUNA ID
    nome = db.Column(db.String(100)) #CRIANDO COLUNA NOME
    servico = db.Column(db.String(100)) #CRIANDO COLUNA SERIVO
    data = db.Column(db.String(20)) #CRIANDO COLUNA DATA
    horario = db.Column(db.String(10)) #CRIANDO COLUNA HORARIO
