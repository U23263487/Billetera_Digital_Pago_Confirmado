from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import db
from models.transaccion import Transaccion

principal_bp = Blueprint("principal", __name__)


@principal_bp.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        valor_monto = request.form.get("monto", "").strip()

        try:
            monto = Decimal(valor_monto)
            if not monto.is_finite() or monto <= 0:
                raise InvalidOperation
            monto = monto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if monto > Decimal("99999999.99"):
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            flash("Ingresa un monto válido mayor que cero.", "error")
            return redirect(url_for("principal.inicio"))

        # Registro académico simulado: no transfiere dinero ni verifica pagos.
        transaccion = Transaccion(
            monto=monto,
            estado="SIMULADO",
            descripcion="Prueba académica de cobro"
        )

        try:
            db.session.add(transaccion)
            db.session.commit()
            flash(
                "Registro de prueba guardado. No se ha realizado ningún pago real.",
                "success"
            )
        except Exception:
            db.session.rollback()
            flash(
                "No se pudo guardar el registro. Revisa la conexión con MySQL.",
                "error"
            )

        return redirect(url_for("principal.inicio"))

    transacciones = (
        Transaccion.query
        .order_by(Transaccion.fecha.desc(), Transaccion.id.desc())
        .limit(10)
        .all()
    )
    return render_template("inicio.html", transacciones=transacciones)
