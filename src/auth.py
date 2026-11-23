# auth.py
# Login por consola: usuario o correo + clave, máximo 3 intentos y bloqueo temporal.

import getpass
import time
import archivos
import config


def usuarios_activos(usuarios):
    """Nombres de usuario que están en estado 'Activo'."""
    return [u["usuario"] for u in usuarios if u["estado"].lower() == "activo"]


def verificar_credenciales(identificador, clave, usuarios):
    """Devuelve la sesión si usuario (o correo) y clave son correctos y el usuario está activo."""
    identificador = identificador.strip().lower()
    for u in usuarios:
        coincide = identificador in (u["usuario"].lower(), u["correo_institucional"].lower())
        if coincide and clave == u["contrasena"] and u["estado"].lower() == "activo":
            return {"usuario": u["usuario"], "nombre": u["nombre_completo"],
                    "correo": u["correo_institucional"], "rol": u["rol"]}
    return None


def pedir_clave():
    """Pide la clave sin mostrarla."""
    try:
        return getpass.getpass("    2. Ingrese Clave   : ")
    except Exception:
        return input("    2. Ingrese Clave   : ")


def bloquear(segundos):
    """Pantalla de bloqueo: cuenta regresiva visible."""
    print(f"\n  Demasiados intentos fallidos. Acceso bloqueado por {segundos} segundos.")
    for restante in range(segundos, 0, -1):
        print(f"\r  Podrá intentarlo de nuevo en {restante:>3} s ...", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 50 + "\r", end="")


def iniciar_sesion():
    """Pide credenciales hasta que sean correctas. Escribir 'cancelar' devuelve None."""
    usuarios = archivos.leer_usuarios()
    print("\n" + "=" * 60)
    print(f"  Bienvenido a {config.NOMBRE_SISTEMA}")
    print("=" * 60)
    print("  Por favor ingrese sus credenciales (escriba 'cancelar' para salir)")
    fallos = 0
    while True:
        identificador = input("\n    1. Ingrese Usuario : ").strip()
        if identificador.lower() == "cancelar":
            return None
        clave = pedir_clave()
        sesion = verificar_credenciales(identificador, clave, usuarios)
        if sesion:
            print(f"\n  Bienvenido/a, {sesion['nombre']} ({sesion['rol']}).")
            return sesion
        fallos += 1
        if fallos < config.MAX_INTENTOS:
            print(f"  Credenciales incorrectas. Intentos restantes: {config.MAX_INTENTOS - fallos}.")
        else:
            bloquear(config.SEGUNDOS_BLOQUEO)
            fallos = 0


if __name__ == "__main__":
    print("Sesión obtenida:", iniciar_sesion())
