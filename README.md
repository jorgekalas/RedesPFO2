# 🗂️ PFO 2 — Sistema de Gestión de Tareas con API REST y Base de Datos

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Werkzeug](https://img.shields.io/badge/Werkzeug-Security-orange)](https://werkzeug.palletsprojects.com/)
[![License](https://img.shields.io/badge/Licencia-Educativa-green)](./LICENSE)

> **Programación Sobre Redes — IFTS N° 29 — Primer Semestre 2026**  
> Autor: **Jorge Kalas** | Docente: **Germán Ríos**

---

##  Descripción

Sistema cliente-servidor desarrollado con **Flask** que expone una API REST para registro y autenticación de usuarios. Los datos se persisten en **SQLite** y las contraseñas se almacenan usando **hash seguro** (nunca en texto plano). El cliente es una aplicación de consola en Python que interactúa con la API mediante solicitudes HTTP.

---

##  Arquitectura

```
┌────────────────┐        HTTP Requests         ┌────────────────────┐        SQL Queries       ┌──────────────┐
│   CLIENTE      │  ──────────────────────────▶  │     SERVIDOR       │  ──────────────────────▶  │  BASE DE     │
│  cliente.py    │  ◀──────────────────────────  │  servidor.py       │  ◀──────────────────────  │  DATOS       │
│  (consola)     │        JSON Responses         │  (Flask API REST)  │        Resultados         │  tareas.db   │
└────────────────┘                               └────────────────────┘                           │  (SQLite)    │
                                                                                                   └──────────────┘
```

---

##  Estructura del Proyecto

```
PFO2/
├── servidor.py              # API REST con Flask
├── cliente.py               # Cliente de consola
├── tareas.db                # Base de datos SQLite (se crea automáticamente)
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

---

##  Endpoints de la API

| Método | Endpoint     | Descripción                          | Código de éxito |
|--------|--------------|--------------------------------------|-----------------|
| `POST` | `/registro`  | Registra un nuevo usuario            | `201 CREATED`   |
| `POST` | `/login`     | Inicia sesión con credenciales       | `200 OK`        |
| `GET`  | `/tareas`    | Página HTML de bienvenida            | `200 OK`        |

###  Formato de los requests

**POST `/registro`** y **POST `/login`** — body JSON:
```json
{
  "usuario": "nombre_de_usuario",
  "contraseña": "mi_contraseña"
}
```

###  Respuestas posibles

| Situación                    | Código | Respuesta                                            |
|------------------------------|--------|------------------------------------------------------|
| Registro exitoso             | `201`  | `{"mensaje": "Usuario registrado correctamente"}`    |
| Login exitoso                | `200`  | `{"mensaje": "Inicio de sesión exitoso"}`            |
| Usuario ya existe            | `409`  | `{"error": "El usuario ya existe"}`                  |
| Credenciales incorrectas     | `401`  | `{"error": "Usuario o contraseña incorrectos"}`      |
| Datos faltantes              | `400`  | `{"error": "Faltan datos obligatorios"}`             |

---

##  Base de Datos

La base de datos se crea automáticamente en `tareas.db` al iniciar el servidor por primera vez.

**Tabla `usuarios`:**

| Campo       | Tipo              | Descripción                         |
|-------------|-------------------|-------------------------------------|
| `id`        | INTEGER (PK)      | Identificador único autoincremental |
| `usuario`   | TEXT NOT NULL UNIQUE | Nombre de usuario (único)        |
| `contraseña`| TEXT NOT NULL     | Contraseña almacenada como hash     |

---

##  Instalación y Ejecución

### Requisitos previos

- Python 3.8 o superior
- pip

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/jorgekalas/RedesPFO2.git
```

### 2. Crear y activar el entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> ✅ Cuando el entorno está activo, el prompt muestra `(venv)` al inicio.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install flask werkzeug requests
```

### 4. Iniciar el servidor

```bash
python servidor.py
```

Deberías ver una salida similar a:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

> ⚠️ **Dejá esta terminal abierta.** El servidor debe estar corriendo para que el cliente funcione.

### 5. Ejecutar el cliente (en una nueva terminal)

Abrí una segunda terminal, activá el entorno virtual nuevamente y ejecutá:

```bash
python cliente.py
```

Verás el menú interactivo:

```
--- MENÚ ---
1. Registrar usuario
2. Iniciar sesión
3. Salir
Elegí una opción:
```

### 6. Probar el endpoint /tareas en el navegador

Con el servidor corriendo, abrí tu navegador y accedé a:

```
http://127.0.0.1:5000/tareas
```

---

## Pruebas con Postman

También podés probar la API directamente con [Postman](https://www.postman.com/) o cualquier cliente HTTP.

### Registrar un usuario

```
POST http://127.0.0.1:5000/registro
Content-Type: application/json

{
  "usuario": "jorge kalas",
  "contraseña": "1234"
}
```

### Iniciar sesión

```
POST http://127.0.0.1:5000/login
Content-Type: application/json

{
  "usuario": "jorge kalas",
  "contraseña": "1234"
}
```

### Ver página de bienvenida

```
GET http://127.0.0.1:5000/tareas
```

---

##  Seguridad: Hash de Contraseñas

Las contraseñas **nunca se almacenan en texto plano**. Se utiliza `generate_password_hash` de Werkzeug, que aplica un algoritmo de hash con salt aleatorio.

```python
# Al registrar
contraseña_hasheada = generate_password_hash(contraseña)

# Al verificar
check_password_hash(hash_almacenado, contraseña_ingresada)
```

**¿Por qué es importante?**
- Si la base de datos fuera comprometida, las contraseñas originales no serían recuperables.
- El salt aleatorio previene ataques de diccionario y rainbow tables.
- Dos usuarios con la misma contraseña tendrán hashes distintos.

---

##  Dependencias

| Paquete      | Versión | Uso                                 |
|--------------|---------|-------------------------------------|
| `Flask`      | 3.x     | Framework para la API REST          |
| `Werkzeug`   | 3.x     | Hashing seguro de contraseñas       |
| `requests`   | 2.x     | Cliente HTTP para el script consola |
| `sqlite3`    | built-in| Base de datos (incluido en Python)  |

---

##  Preguntas frecuentes

**¿Dónde se guarda la base de datos?**  
En el archivo `tareas.db` dentro del directorio del proyecto. Se crea automáticamente al iniciar el servidor por primera vez.

**¿Puedo usar la API desde otro cliente (no el script de consola)?**  
Sí. Cualquier cliente HTTP que envíe JSON funciona: Postman, curl, Insomnia, o desde otro script Python.

**¿El servidor usa HTTPS?**  
No, corre en HTTP local (127.0.0.1). Para producción se debería configurar HTTPS y un servidor WSGI como Gunicorn.

**¿Qué pasa si intento registrar el mismo usuario dos veces?**  
El servidor devuelve `409 CONFLICT` porque el campo `usuario` tiene restricción `UNIQUE` en la base de datos.

---

##  Autor

**Jorge Kalas**  
IFTS N° 29 — Tecnicatura Superior en Desarrollo de Software 
Programación Sobre Redes — Primer Semestre 2026  
Docente: Germán Ríos

---
