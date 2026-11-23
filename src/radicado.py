# radicado.py
# Arma el comprobante (radicado) en texto, con marco ASCII (+ - |).
# CADA línea mide exactamente 120 caracteres. No incluye la descripción detallada.

import textwrap
from datetime import datetime
import config

ANCHO = config.ANCHO_RADICADO       # 120
INTERNO = ANCHO - 2                 # espacio entre las dos barras '|'
COLUMNA_ETIQUETA = 28
ANCHO_VALOR = INTERNO - 2 - COLUMNA_ETIQUETA


def numero_radicado(tipo, id_registro):
    """Ej.: Peticion y 3001 -> 'PET-003001'."""
    return f"{config.PREFIJOS[tipo]}-{int(id_registro):06d}"


def _borde():
    return "+" + "-" * INTERNO + "+"


def _seccion(titulo):
    return "+" + f" {titulo} ".center(INTERNO, "-") + "+"


def _centrada(texto):
    return "|" + texto.center(INTERNO) + "|"


def _campo(etiqueta, valor):
    """Una fila 'Etiqueta : valor'. Si el valor es muy largo, sigue alineado."""
    partes = textwrap.wrap(str(valor) or "N/A", ANCHO_VALOR, break_long_words=True) or ["N/A"]
    filas = []
    for i, parte in enumerate(partes):
        titulo = f"{etiqueta:<{COLUMNA_ETIQUETA - 2}}: " if i == 0 else " " * COLUMNA_ETIQUETA
        filas.append("|" + (" " + titulo + parte).ljust(INTERNO) + "|")
    return filas


def generar_radicado(registro):
    """Devuelve el comprobante completo como texto."""
    tipo = registro["tipo_solicitud"]
    direccion = registro.get("direccion", "").strip() or "N/A"
    lineas = [
        _borde(),
        _centrada(config.NOMBRE_SISTEMA.upper()),
        _centrada(config.INSTITUCION),
        _centrada("COMPROBANTE DE RADICACIÓN DE PQRS"),
        _seccion("DATOS DEL RADICADO"),
        *_campo("Número de radicado", numero_radicado(tipo, registro["id"])),
        *_campo("ID de registro", f"{int(registro['id']):06d}"),
        *_campo("Fecha y hora de radicación", registro["fecha_radicacion"]),
        *_campo("Estado", registro["estado_peticion"]),
        *_campo("Fecha máxima de respuesta", registro["fecha_maxima_respuesta"]),
        *_campo("Registrado por", registro["usuario_registro"]),
        _seccion("DATOS DEL SOLICITANTE"),
        *_campo("Nombre completo", registro["nombre_completo"]),
        *_campo("Documento", f"{registro['tipo_documento']} {registro['numero_documento']}"),
        *_campo("Teléfono de contacto", f"{registro['telefono_contacto']} ({registro['tipo_telefono']})"),
        *_campo("Correo electrónico", registro["correo_electronico"]),
        *_campo("Dirección", direccion),
        _seccion("CLASIFICACIÓN"),
        *_campo("Tipo de solicitud", config.ETIQUETAS_TIPO[tipo]),
        *_campo("Canal de recepción", registro["canal_recepcion"]),
        *_campo("Tipo de mascota", registro["tipo_mascota"]),
        *_campo("Campus relacionado", registro["campus_relacionado"]),
        _seccion("RESUMEN"),
        *_campo("Asunto o título", registro["asunto_titulo"]),
        _seccion("CERTIFICACIÓN"),
        _centrada("Este comprobante certifica la información registrada en el sistema de PQRS."),
        _centrada("Generado el " + datetime.now().strftime(config.FORMATO_FECHA)),
        _borde(),
    ]
    mal = [linea for linea in lineas if len(linea) != ANCHO]
    if mal:
        raise ValueError(f"Una línea del radicado no mide {ANCHO} caracteres: {mal[0]!r}")
    return "\n".join(lineas) + "\n"


def guardar_radicado(registro):
    """Guarda el radicado como archivo .txt y devuelve la ruta."""
    config.CARPETA_RADICADOS.mkdir(parents=True, exist_ok=True)
    ruta = config.CARPETA_RADICADOS / f"{numero_radicado(registro['tipo_solicitud'], registro['id'])}.txt"
    ruta.write_text(generar_radicado(registro), encoding="utf-8", newline="\n")
    return ruta


if __name__ == "__main__":
    import archivos
    primera_peticion = archivos.leer_registros("Peticion")[0]
    print(generar_radicado(primera_peticion))
