from flask import Flask, request, jsonify, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Nombre de la base de datos SQLite
DB_NAME = "tareas.db"


def crear_base_de_datos():
    """
    Crea la base de datos y la tabla de usuarios si no existen.
    """
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def obtener_usuario(nombre_usuario):
    """
    Busca un usuario en la base de datos por su nombre.
    """
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, usuario, contraseña FROM usuarios WHERE usuario = ?",
        (nombre_usuario,)
    )

    usuario = cursor.fetchone()
    conexion.close()

    return usuario


@app.route("/registro", methods=["POST"])
def registro():
    """
    Endpoint para registrar usuarios.
    Recibe un usuario y una contraseña, hashea la contraseña
    y guarda los datos en SQLite.
    """
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    contraseña_hasheada = generate_password_hash(contraseña)

    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios (usuario, contraseña)
            VALUES (?, ?)
        """, (usuario, contraseña_hasheada))

        conexion.commit()
        conexion.close()

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    except sqlite3.Error as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@app.route("/login", methods=["POST"])
def login():
    """
    Endpoint para iniciar sesión.
    Verifica si el usuario existe y si la contraseña ingresada
    coincide con la contraseña hasheada guardada en la base de datos.
    """
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    usuario_encontrado = obtener_usuario(usuario)

    if usuario_encontrado is None:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    contraseña_guardada = usuario_encontrado[2]

    if check_password_hash(contraseña_guardada, contraseña):
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200

    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


@app.route("/tareas", methods=["GET"])
def tareas():
    """
    Endpoint que muestra un HTML simple de bienvenida.
    """
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Tareas</title>
    </head>
    <body>
        <h1>Bienvenido al sistema de gestión de tareas</h1>
        <p>La API Flask está funcionando correctamente.</p>
        <p>Endpoints disponibles:</p>
        <ul>
            <li>POST /registro</li>
            <li>POST /login</li>
            <li>GET /tareas</li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    crear_base_de_datos()
    app.run(debug=True, host="127.0.0.1", port=5000)