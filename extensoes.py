# Arquivo separado para evitar importação circular
# db é o objeto que conecta o Flask ao banco de dados
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()