""" IMPORTANDO AS BIBLIOTECAS """
from flask_sqlalchemy import SQLAlchemy

""" CRIA A VARIAVEL DB QUE VAI SER USADA NO MAIN.PY """
db = SQLAlchemy()

""" TABELA DE USUARIOS """
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Relacionamento: um usuario tem muitos agendamentos
    agendamentos = db.relationship('Agendamento', backref='usuario', lazy=True)

""" TABELA DE AGENDAMENTOS """
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Chave estrangeira: liga o agendamento ao usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    servico = db.Column(db.String(100))
    data = db.Column(db.String(20))
    horario = db.Column(db.String(10))
