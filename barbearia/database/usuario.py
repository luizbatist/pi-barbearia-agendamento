""" IMPORTANDO AS BIBLIOTECAS """
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario

def criar_usuario(nome, email, senha):
    """ Cria um novo usuario com a senha criptografada """
    senha_hash = generate_password_hash(senha)
    usuario = Usuario(nome=nome, email=email, senha=senha_hash)
    db.session.add(usuario)
    db.session.commit()

def buscar_usuario_por_email(email):
    """ Busca um usuario pelo email """
    return Usuario.query.filter_by(email=email).first()

def verificar_senha(usuario, senha):
    """ Verifica se a senha digitada bate com a senha salva """
    return check_password_hash(usuario.senha, senha)
