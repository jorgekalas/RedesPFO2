import requests

# URL base del servidor
BASE_URL = "http://127.0.0.1:5000"


def registrar_usuario():
    usuario = input("Ingresá usuario: ")
    contraseña = input("Ingresá contraseña: ")

    data = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    response = requests.post(f"{BASE_URL}/registro", json=data)
    print(response.json())


def login_usuario():
    usuario = input("Ingresá usuario: ")
    contraseña = input("Ingresá contraseña: ")

    data = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    response = requests.post(f"{BASE_URL}/login", json=data)
    print(response.json())


def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            login_usuario()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()