import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
url = os.getenv("DATABASE_URL")

if not url:
    raise RuntimeError("No se encontró DATABASE_URL. Revisa el archivo .env.")

try:
    engine = create_engine(url, pool_pre_ping=True)
    with engine.connect() as conexion:
        version = conexion.execute(text("SELECT VERSION()")).scalar()
    print("CONEXIÓN EXITOSA CON MYSQL")
    print("Versión de MySQL:", version)
except Exception as error:
    print("NO SE PUDO CONECTAR A MYSQL")
    print("Detalle del error:", error)
