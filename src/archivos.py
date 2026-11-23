# archivos.py
# Lee y escribe los archivos planos (Peticion.txt, Queja.txt, Reclamo.txt, Sugerencia.txt)
# y el archivo de usuarios. Las columnas de cada línea van separadas por "|".

import os
import tempfile
import config


def ruta_archivo(tipo):
    """Devuelve la ruta del archivo de un tipo. Ej.: 'Queja' -> data/Queja.txt"""
    return config.CARPETA_DATA / config.ARCHIVOS_PQRS[tipo]


def limpiar_texto(valor):
    """Evita que un texto dañe el formato: cambia '|' por '/' y quita saltos de línea."""
    return str(valor).replace(config.SEPARADOR, "/").replace("\r", " ").replace("\n", " ").strip()


def leer_registros(tipo):
    """Lee el archivo y devuelve una lista de diccionarios (un diccionario por PQRS)."""
    ruta = ruta_archivo(tipo)
    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(config.SEPARADOR.join(config.CAMPOS) + "\n", encoding="utf-8")
    registros = []
    with open(ruta, encoding="utf-8-sig") as archivo:
        encabezado = archivo.readline().rstrip("\r\n").split(config.SEPARADOR)
        for linea in archivo:
            valores = linea.rstrip("\r\n").split(config.SEPARADOR)
            if len(valores) == len(encabezado):
                registros.append(dict(zip(encabezado, valores)))
    return registros


def ultimo_id(tipo):
    """El ID más alto que hay en el archivo (0 si está vacío)."""
    ids = [int(r["id"]) for r in leer_registros(tipo) if r["id"].isdigit()]
    return max(ids, default=0)


def siguiente_id(tipo):
    """El consecutivo: el ID más alto + 1. Con las bases del profe empieza en 3001."""
    return ultimo_id(tipo) + 1


def buscar_registro(tipo, id_registro):
    """Devuelve la PQRS con ese ID, o None si no existe."""
    for registro in leer_registros(tipo):
        if registro["id"] == str(id_registro):
            return registro
    return None


def guardar_registro(tipo, datos):
    """Agrega una PQRS nueva al final del archivo. Le asigna el siguiente ID."""
    if not str(datos.get("usuario_registro", "")).strip():
        raise ValueError("No se puede guardar una PQRS sin usuario registrador.")
    registro = dict(datos)
    registro["id"] = str(siguiente_id(tipo))
    registro["tipo_solicitud"] = tipo
    linea = config.SEPARADOR.join(limpiar_texto(registro[campo]) for campo in config.CAMPOS)

    ruta = ruta_archivo(tipo)
    with open(ruta, "rb+") as archivo:
        archivo.seek(0, os.SEEK_END)
        if archivo.tell() > 0:
            archivo.seek(-1, os.SEEK_END)
            if archivo.read(1) != b"\n":
                archivo.write(b"\n")
    with open(ruta, "a", encoding="utf-8", newline="\n") as archivo:
        archivo.write(linea + "\n")
    return registro


def actualizar_estado(tipo, id_registro, nuevo_estado):
    """Cambia el estado de UNA PQRS de forma segura usando un archivo temporal."""
    registros = leer_registros(tipo)
    encontrado = False
    for registro in registros:
        if registro["id"] == str(id_registro):
            registro["estado_peticion"] = nuevo_estado
            encontrado = True
    if not encontrado:
        raise ValueError(f"No existe {tipo} con ID {id_registro}.")

    ruta = ruta_archivo(tipo)
    descriptor, temporal = tempfile.mkstemp(dir=ruta.parent, suffix=".tmp")
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as archivo:
        archivo.write(config.SEPARADOR.join(config.CAMPOS) + "\n")
        for registro in registros:
            archivo.write(config.SEPARADOR.join(limpiar_texto(registro[c]) for c in config.CAMPOS) + "\n")
    os.replace(temporal, ruta)


def leer_usuarios():
    """Lee Usuarios.txt y devuelve una lista de diccionarios."""
    ruta = config.CARPETA_DATA / config.ARCHIVO_USUARIOS
    with open(ruta, encoding="utf-8-sig") as archivo:
        encabezado = archivo.readline().rstrip("\r\n").split(config.SEPARADOR)
        return [dict(zip(encabezado, linea.rstrip("\r\n").split(config.SEPARADOR)))
                for linea in archivo if linea.strip()]


if __name__ == "__main__":
    for tipo in config.ARCHIVOS_PQRS:
        print(f"{tipo:<11} registros: {len(leer_registros(tipo)):>5}   "
              f"último ID: {ultimo_id(tipo)}   siguiente ID: {siguiente_id(tipo)}")
