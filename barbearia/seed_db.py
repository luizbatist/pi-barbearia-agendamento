import os
import random
from datetime import datetime, timedelta
from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, Usuario, Agendamento

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, '../instance')

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

db_path = os.path.join(instance_path, 'barbearia.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

nomes = ["Gabriel", "Lucas", "Mateus", "Enzo", "Guilherme", "Rafael", "João", "Felipe", "Gustavo", "Leonardo", "Rodrigo", "Thiago", "Bruno", "Caio", "Diego", "Samuel", "Daniel", "Vitor", "Marcos", "Andre"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa"]

def povoar():
    with app.app_context():
        print(f"Tentando criar o banco em: {db_path}")

        print("Recriando tabelas...")
        db.drop_all()
        db.create_all()

        senha_admin_hash = generate_password_hash("123456")
        admin = Usuario(
            nome="admin",
            email="admin@admin.com",
            senha=senha_admin_hash,
            is_admin=True
        )
        db.session.add(admin)
        print(f"Admin criado: {admin.email}")

        servicos = ["Corte", "Barba", "Corte e Barba", "Degradê", "Pigmentação"]
        horarios = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

        hoje = datetime.now()
        datas_disponiveis = [(hoje + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)]

        todos_os_slots_possiveis = [(data, horario) for data in datas_disponiveis for horario in horarios]

        slots_sorteados = random.sample(todos_os_slots_possiveis, 20)

        senha_cliente_hash = generate_password_hash("123456")

        print("Gerando usuários e agendamentos únicos...")
        for i in range(20):
            nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            email_user = f"{nome_completo.replace(' ', '.').lower()}{random.randint(10, 99)}@email.com"

            novo_usuario = Usuario(
                nome=nome_completo,
                email=email_user,
                senha=senha_cliente_hash,
                is_admin=False
            )
            db.session.add(novo_usuario)
            db.session.flush()

            data_escolhida, horario_escolhido = slots_sorteados[i]

            novo_agendamento = Agendamento(
                usuario_id=novo_usuario.id,
                servico=random.choice(servicos),
                data=data_escolhida,
                horario=horario_escolhido,
                status="Agendado"
            )
            db.session.add(novo_agendamento)

        db.session.commit()
        print("Concluído! Banco populado com 20 agendamentos perfeitamente distribuídos.")

if __name__ == "__main__":
    povoar()