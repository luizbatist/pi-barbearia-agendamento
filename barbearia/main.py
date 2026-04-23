"""  IMPORTANDO BIBLIOTECAS  """
from flask import Flask
from models import db
""" IMPORTANDO AS ROTAS"""
from routes.agendamento import agendamento_route

app = Flask(__name__)
""" SQL LITE EMBAIXO"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbearia.db' 


""" CONECTA O BANCO DE DADOS DB A APLICAÇÃO APP"""
db.init_app(app)

""" CRIANDO TABELAS NO BANCO DE DADOS"""
with app.app_context():
    db.create_all()

""" REGISTRA AS ROTAS DE AGENDAMENTO DA APLICAÇÃO"""
app.register_blueprint(agendamento_route)

""" INICIANDO O SERVER"""
app.run(debug=True)
