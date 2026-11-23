# validaciones.py
# Funciones que revisan cada dato de una PQRS.
# Cada función recibe el texto que escribió la persona:
#   - si el dato es válido, lo devuelve limpio;
#   - si no lo es, lanza un ValueError con un mensaje que explica qué falló.

import re
from datetime import datetime

LETRAS = "A-Za-zÁÉÍÓÚÜáéíóúüÑñ"


def limpiar(texto):
    """Quita espacios de más: al inicio, al final y repetidos entre palabras."""
    return " ".join(str(texto).split())


def validar_nombre(texto):
    nombre = limpiar(texto)
    if nombre == "":
        raise ValueError("El nombre es obligatorio.")
    if not 3 <= len(nombre) <= 100:
        raise ValueError("El nombre debe tener entre 3 y 100 caracteres.")
    if any(caracter.isdigit() for caracter in nombre):
        raise ValueError("El nombre no puede tener números.")
    if not re.fullmatch(rf"[{LETRAS}'\- ]+", nombre):
        raise ValueError("Solo se permiten letras, espacios, apóstrofes (') y guiones (-).")
    return nombre


def validar_numero_documento(texto):
    numero = str(texto).strip()
    if not re.fullmatch(r"\d{3,15}", numero):
        raise ValueError("El documento debe tener solo números, entre 3 y 15 dígitos.")
    return numero


def validar_telefono(texto):
    telefono = str(texto).strip()
    if not re.fullmatch(r"\d{10}", telefono):
        raise ValueError("El teléfono debe tener exactamente 10 dígitos, sin letras.")
    return telefono


def validar_correo(texto):
    correo = str(texto).strip()
    if correo == "":
        raise ValueError("El correo es obligatorio.")
    if len(correo) > 254:
        raise ValueError("El correo no puede tener más de 254 caracteres.")
    if correo.count("@") != 1:
        raise ValueError("El correo debe tener un único @.")
    if not re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}", correo):
        raise ValueError("Formato inválido. Ejemplo: usuario@correo.com")
    return correo


def validar_direccion(texto):
    """La dirección es opcional: si la dejan vacía se guarda como 'N/A'."""
    direccion = limpiar(texto)
    if direccion == "" or direccion.upper() == "N/A":
        return "N/A"
    if not 5 <= len(direccion) <= 200:
        raise ValueError("La dirección debe tener entre 5 y 200 caracteres.")
    if not re.fullmatch(rf"[{LETRAS}0-9 #\-./,]+", direccion):
        raise ValueError("Solo se permiten letras, números y los signos # - . / ,")
    return direccion


def validar_asunto(texto):
    asunto = limpiar(texto)
    if not 5 <= len(asunto) <= 150:
        raise ValueError("El asunto debe tener entre 5 y 150 caracteres.")
    if not re.fullmatch(rf"[{LETRAS}0-9 .,;:¿?¡!()\"'\-/]+", asunto):
        raise ValueError("El asunto solo permite letras, números y signos básicos.")
    return asunto


def validar_descripcion(texto):
    descripcion = limpiar(texto)
    if descripcion == "":
        raise ValueError("La descripción no puede estar vacía.")
    if len(descripcion) < 20:
        raise ValueError("La descripción debe tener al menos 20 caracteres.")
    if len(descripcion) > 2000:
        raise ValueError("La descripción no puede pasar de 2000 caracteres.")
    return descripcion


def validar_fecha(texto, formato="%Y-%m-%d %H:%M:%S"):
    """Convierte el texto en fecha. No se permiten fechas futuras."""
    try:
        fecha = datetime.strptime(str(texto).strip(), formato)
    except ValueError:
        raise ValueError("Fecha inválida. Use el formato AAAA-MM-DD HH:MM:SS")
    if fecha > datetime.now():
        raise ValueError("La fecha de radicación no puede ser futura.")
    return fecha


def validar_opcion(texto, opciones):
    """La persona escribe el número de la opción (1, 2, 3...) o el texto exacto."""
    texto = str(texto).strip()
    if texto.isdigit() and 1 <= int(texto) <= len(opciones):
        return opciones[int(texto) - 1]
    for opcion in opciones:
        if texto.lower() == opcion.lower():
            return opcion
    raise ValueError(f"Opción inválida. Elija un número entre 1 y {len(opciones)}.")


def validar_cambio_estado(actual, nuevo, estados=("Registrada", "En proceso", "Solucionada")):
    """Solo se puede avanzar un paso: Registrada -> En proceso -> Solucionada."""
    if estados.index(nuevo) != estados.index(actual) + 1:
        raise ValueError("Cambio de estado no permitido. Solo se avanza al siguiente estado.")
    return nuevo


if __name__ == "__main__":
    pruebas = [
        (validar_nombre, "Juan David Pérez Gómez", True),
        (validar_nombre, "Juan123", False),
        (validar_nombre, "Ju", False),
        (validar_numero_documento, "1037654321", True),
        (validar_numero_documento, "10376A321", False),
        (validar_telefono, "3001234567", True),
        (validar_telefono, "300123ABCD", False),
        (validar_correo, "usuario@correo.com", True),
        (validar_correo, "usuariocorreo.com", False),
        (validar_direccion, "", True),
        (validar_direccion, "Avenida Siempreviva 742", True),
        (validar_asunto, "Solicitud de información veterinaria", True),
        (validar_asunto, "Hola", False),
        (validar_descripcion, "Solicito información sobre consulta para caninos.", True),
        (validar_descripcion, "muy corta", False),
        (validar_fecha, "2026-09-28 10:30:00", True),
        (validar_fecha, "2099-01-01 10:30:00", False),
    ]
    fallos = 0
    for funcion, dato, debe_pasar in pruebas:
        try:
            funcion(dato)
            paso = True
        except ValueError:
            paso = False
        if paso == debe_pasar:
            print("OK     ", funcion.__name__, repr(dato))
        else:
            print("FALLO  ", funcion.__name__, repr(dato))
            fallos += 1
    print()
    print("Todo bien." if fallos == 0 else f"Hubo {fallos} prueba(s) con problemas.")
