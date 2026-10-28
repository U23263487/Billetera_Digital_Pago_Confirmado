# Billetera_Digital — Pago Confirmado

Proyecto académico base con Python, Flask, MySQL y arquitectura MVC.

## Estructura MVC

- **Modelo (`models/`)**: define las tablas `Usuario` y `Transaccion`.
- **Vista (`templates/` y `static/`)**: HTML con Jinja2 y estilos CSS.
- **Controlador (`controllers/`)**: procesa el formulario y consulta/guarda operaciones.
- **`app.py`**: configura Flask, conecta SQLAlchemy y registra las rutas.

## 1. Requisitos

- Python instalado.
- MySQL Server y MySQL Workbench.
- Visual Studio Code.

## 2. Crear la base de datos

Abre MySQL Workbench, conecta con tu servidor y ejecuta el contenido de
`database/crear_base_datos.sql`.

## 3. Preparar el entorno en VS Code

Abre la carpeta `Billetera_Digital` en VS Code y abre la terminal.

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si la activación de PowerShell está permitida, también puedes usar:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 4. Configurar MySQL

1. Duplica `.env.example`.
2. Renombra la copia a `.env` (sin `.example`).
3. Edita `DATABASE_URL` y reemplaza `TU_CLAVE_MYSQL` por tu contraseña local.

Ejemplo si tu usuario MySQL es `root` y la contraseña es `MiClave123`:

```text
DATABASE_URL=mysql+pymysql://root:MiClave123@localhost:3306/billetera_digital
```

No compartas tu archivo `.env` ni publiques contraseñas. Si la contraseña contiene
caracteres como `@`, `#`, `/` o `:`, puede necesitar codificación URL.

## 5. Probar la conexión

```powershell
.\.venv\Scripts\python.exe probar_conexion.py
```

Debe mostrar `CONEXIÓN EXITOSA CON MYSQL`. Si no ocurre, revisa que MySQL Server esté
encendido, que la contraseña sea correcta y que el nombre de la base de datos coincida.

## 6. Ejecutar el sistema

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre en el navegador: http://127.0.0.1:5000

Registra un monto de prueba y comprueba que aparezca en el historial.

## 7. Comprobar los registros en Workbench

```sql
USE billetera_digital;
SHOW TABLES;

SELECT id, monto, estado, descripcion, fecha
FROM transacciones
ORDER BY id DESC;
```

## Importante sobre los pagos

Esta versión registra operaciones **simuladas** para probar el flujo MVC y la conexión
con MySQL. No genera códigos QR de pago, no se conecta a bancos o billeteras reales,
no verifica capturas de pantalla y no transfiere dinero. Para pagos reales se necesitaría
integrar un proveedor autorizado y verificar sus notificaciones desde el servidor.

## Nota de desarrollo

`db.create_all()` crea tablas que no existen, pero no modifica automáticamente tablas
existentes si cambias tus modelos. Para siguientes etapas se recomienda usar migraciones.
