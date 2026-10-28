from flask import Flask, render_template, request, jsonify
from config import Config
from models import db
from models.usuario import Usuario  
from models.transaccion import Transaccion
from controllers.principal_controller import principal_bp

def crear_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "No se encontró DATABASE_URL. Revisa el archivo .env y config.py."
        )

    db.init_app(app)
    
    # ================= RUTA 1: INICIO =================
    @app.route('/')
    def inicio():
        try:
            transacciones_db = Transaccion.query.order_by(Transaccion.id.desc()).all()
            lista_transacciones = []
            total_ventas = 0.0
            
            for t in transacciones_db:
                fecha_str = t.fecha.strftime('%Y-%m-%d %H:%M:%S') if hasattr(t.fecha, 'strftime') else str(t.fecha)
                lista_transacciones.append({
                    "monto": float(t.monto),
                    "fecha": fecha_str
                })
                total_ventas += float(t.monto)
                
            num_transacciones = len(lista_transacciones)
        except Exception as e:
            print(f"Error consultando base de datos: {e}")
            lista_transacciones = []
            total_ventas = 0.0
            num_transacciones = 0

        return render_template('inicio.html', 
                               active_page='inicio', 
                               transacciones=lista_transacciones, 
                               total_ventas=total_ventas,
                               num_transacciones=num_transacciones)

    # ================= RUTA 2: COBRAR VISTA =================
    @app.route('/cobrar')
    def cobrar_vista():
        return render_template('cobrar.html', active_page='cobrar')

    # ================= RUTA 3: PROCESAR REGISTRO =================
    @app.route('/registrar', methods=['POST'])
    def registrar():
        monto = request.form.get('monto')
        if monto:
            try:
                nueva_transaccion = Transaccion(monto=float(monto))
                db.session.add(nueva_transaccion)
                db.session.commit()
                return jsonify({"status": "success"}), 200
            except Exception as e:
                db.session.rollback()
                print(f"Error al guardar en BD: {e}")
                return jsonify({"status": "error"}), 500
        return jsonify({"status": "bad request"}), 400

    # ================= NUEVA RUTA 4: HISTORIAL DE OPERACIONES INDEPENDIENTE =================
    @app.route('/historial')
    def historial_vista():
        try:
            transacciones_db = Transaccion.query.order_by(Transaccion.id.desc()).all()
            lista_transacciones = []
            total_ventas = 0.0
            
            for t in transacciones_db:
                fecha_str = t.fecha.strftime('%Y-%m-%d %H:%M:%S') if hasattr(t.fecha, 'strftime') else str(t.fecha)
                lista_transacciones.append({
                    "monto": float(t.monto),
                    "fecha": fecha_str
                })
                total_ventas += float(t.monto)
        except Exception as e:
            print(f"Error consultando historial en BD: {e}")
            lista_transacciones = []
            total_ventas = 0.0

        return render_template('historial.html', 
                               active_page='historial', 
                               transacciones=lista_transacciones, 
                               total_ventas=total_ventas)

    # ================= NUEVA RUTA 5: PERFIL PROTOPERSONA INDEPENDIENTE =================
    @app.route('/perfil')
    def perfil_vista():
        return render_template('perfil.html', active_page='perfil')

    app.register_blueprint(principal_bp)

    with app.app_context():
        db.create_all()

    return app

app = crear_app()

if __name__ == "__main__":
    app.run(debug=True)
