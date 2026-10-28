from datetime import datetime
from models import db


class Transaccion(db.Model):
    __tablename__ = "transacciones"

    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="SIMULADO")
    descripcion = db.Column(db.String(200))
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )
    usuario = db.relationship("Usuario", back_populates="transacciones")
