from models import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    # Se almacena el hash de la contraseña, nunca la contraseña en texto plano.
    password_hash = db.Column(db.String(255), nullable=False)

    transacciones = db.relationship(
        "Transaccion",
        back_populates="usuario",
        lazy=True
    )
