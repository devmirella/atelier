# Importa o objeto db que será criado no app.py
from extensoes import db 

# Tabela: inpirações 
class Inspiracao(db.Model):
    # Nome da tabela no banco de dados
    __tablename__ = "inspiracoes"

    # Colunas da tabela
    id      = db.Column(db.Integer, primary_key=True)
    imagem  = db.Column(db.String(300), nullable=False)

# Tabela: Arte
class Arte(db.Model):
    __tablename__ = "artes"
    id      = db.Column(db.Integer, primary_key=True)
    imagem  = db.Column(db.String(300), nullable=False)

# Tabela: Exposed 
class Exposed(db.Model):
    __tablename__ = "exposed"
    id      = db.Column(db.Integer, primary_key=True)
    imagem  = db.Column(db.String(300), nullable=False)
    titulo  = db.Column(db.String(200), nullable=True)
    tag     = db.Column(db.String(100), nullable=True)

    # Relacionamento com as artes internas 
    artes   = db.relationship("ArteInterna", backref="exposed", cascade="all, delete-orphan")

# Tabela: Artes internas 
class ArteInterna(db.Model):
    __tablename__ = "artes_internas"
    id          = db.Column(db.Integer, primary_key=True)
    imagem      = db.Column(db.String(300), nullable=False)
    # exposed_id liga essa arte a um card da tabela exposed
    exposed_id  = db.Column(db.Integer, db.ForeignKey("exposed.id"), nullable=False)