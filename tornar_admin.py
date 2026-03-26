from app import app, db
from models import Usuario

with app.app_context():
    usuario = Usuario.query.filter_by(email="marinasillva43@gmail.com").first()
    usuario.is_admin = True
    db.session.commit()
    print("Feito!")