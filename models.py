# Importa o objeto db que será criado no app.py
from extensoes import db 
from flask_login import UserMixin

# Tabela: Usuários 
# Define a tabela de usuários no banco (db.Model) e adiciona recursos de autenticação (UserMixin)
class Usuario(db.Model, UserMixin):
   
    # Define o nome da tabela no banco
    __tablename__ = "usuarios"
    
    # Colunas da tabela
    id       = db.Column(db.Integer, primary_key=True) # ID único do usuário (chave primária)
    email    = db.Column(db.String(150), unique=True, nullable=False) # Email do usuário (não pode repetir e não pode ser vazio)
    senha    = db.Column(db.String(200), nullable=False) # Senha do usuário (obrigatória)
    nome     = db.Column(db.String(1000), nullable=False) # Nome do usuário (obrigatório)
    is_admin = db.Column(db.Boolean, default=False) # Indica se o usuário é administrador (padrão: não é)
    ativo    = db.Column(db.Boolean, default=True)

    artes       = db.relationship("Arte", backref="dono",cascade="all, delete-orphan" )
    inspiracoes = db.relationship("Inspiracao", backref="dono", cascade="all, delete-orphan")
    exposed     = db.relationship("Exposed", backref="dono", cascade="all, delete-orphan")

# Tabela: inspirações 
class Inspiracao(db.Model):
    
    __tablename__ = "inspiracoes"

    id          = db.Column(db.Integer, primary_key=True)
    imagem      = db.Column(db.String(300), nullable=False)
    usuario_id  = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False )

# Tabela: Arte
class Arte(db.Model): 

    __tablename__ = "artes"

    id          = db.Column(db.Integer, primary_key=True)
    imagem      = db.Column(db.String(300), nullable=False)
    usuario_id  = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

# Tabela: Exposed 
class Exposed(db.Model):

    __tablename__ = "exposed"

    id          = db.Column(db.Integer, primary_key=True)
    imagem      = db.Column(db.String(300), nullable=False)
    titulo      = db.Column(db.String(200), nullable=True)
    tag         = db.Column(db.String(100), nullable=True)
    usuario_id  = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    # Relacionamento com as artes internas 
    artes   = db.relationship("ArteInterna", backref="exposed", cascade="all, delete-orphan")

# Tabela: Artes internas 
class ArteInterna(db.Model):

    __tablename__ = "artes_internas"

    id          = db.Column(db.Integer, primary_key=True)
    imagem      = db.Column(db.String(300), nullable=False)
    # exposed_id liga essa arte a um card da tabela exposed
    exposed_id  = db.Column(db.Integer, db.ForeignKey("exposed.id"), nullable=False)