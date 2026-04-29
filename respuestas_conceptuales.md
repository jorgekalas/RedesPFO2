# Respuestas Conceptuales — PFO 2

## 1. ¿Por qué hashear contraseñas?

Almacenar contraseñas en texto plano es un riesgo crítico de seguridad. Si alguien accede a la base de datos —por un ataque, una copia de seguridad expuesta o un error humano— tendría acceso inmediato a las credenciales de todos los usuarios.

Una función de **hash** transforma la contraseña original en una cadena irreversible de longitud fija. Esto significa que, incluso con acceso directo a la base de datos, no es posible recuperar la contraseña original.

En este proyecto se usa `generate_password_hash` de **Werkzeug**, que aplica un algoritmo seguro con **salt aleatorio** por cada contraseña. Esto tiene dos ventajas clave:

- **Previene ataques de diccionario**: no se puede comparar el hash con listas de contraseñas conocidas.
- **Previene rainbow tables**: aunque dos usuarios tengan la misma contraseña, sus hashes serán completamente distintos.

La verificación se hace con `check_password_hash`, que compara la contraseña ingresada contra el hash almacenado **sin necesidad de descifrar nada**. El sistema nunca necesita conocer la contraseña original.

```python
# Al registrar un usuario
contraseña_hasheada = generate_password_hash("mi_contraseña")
# Resultado: "scrypt:32768:8:1$abc123$f9e8d7c6b5a4..."

# Al verificar en el login
check_password_hash(contraseña_hasheada, "mi_contraseña")  # True
check_password_hash(contraseña_hasheada, "otra_cosa")      # False
```

> **Conclusión:** hashear contraseñas protege a los usuarios incluso ante una brecha de seguridad en la base de datos. Es una práctica obligatoria en cualquier sistema que maneje credenciales.

---

## 2. Ventajas de usar SQLite en este proyecto

**SQLite** es un motor de base de datos relacional embebido: no requiere instalar ni configurar un servidor separado. Toda la base de datos vive en un único archivo (`tareas.db`).

### Ventajas en el contexto de este proyecto

| Ventaja | Detalle |
|---|---|
| **Sin instalación** | No requiere MySQL, PostgreSQL ni ningún servidor externo |
| **Integración nativa** | El módulo `sqlite3` viene incluido en Python, sin dependencias extra |
| **Portabilidad** | Todo el proyecto se puede mover o compartir copiando una sola carpeta |
| **Ligereza** | No consume recursos del sistema al no correr como servicio en segundo plano |
| **Ideal para desarrollo** | Perfecto para proyectos educativos, prototipos y aplicaciones de pequeña escala |

### Limitación a tener en cuenta

SQLite no está diseñado para manejar muchas escrituras concurrentes. Para un sistema en producción con múltiples usuarios simultáneos se debería migrar a **PostgreSQL** o **MySQL**.

> **Conclusión:** SQLite es la elección correcta para este proyecto por su simplicidad y por no requerir infraestructura adicional, sin sacrificar ninguna funcionalidad necesaria para el alcance de la PFO.
