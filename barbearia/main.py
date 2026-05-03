""" IMPORTANDO BIBLIOTECAS """
from flask import Flask
from models import db
""" IMPORTANDO AS ROTAS """
from routes.agendamento import agendamento_route
from routes.auth import auth_route

app = Flask(__name__)

""" CHAVE SECRETA PARA A SESSAO DE LOGIN """
app.config['SECRET_KEY'] = 'barbearia-rafa-darc-2026'

""" BANCO DE DADOS SQLITE """
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbearia.db'

""" CONECTA O BANCO DE DADOS À APLICAÇÃO """
db.init_app(app)

""" CRIANDO TABELAS NO BANCO DE DADOS """
with app.app_context():
    db.create_all()

""" REGISTRANDO AS ROTAS """
app.register_blueprint(agendamento_route)
app.register_blueprint(auth_route)

""" INICIANDO O SERVER """
app.run(debug=False)
