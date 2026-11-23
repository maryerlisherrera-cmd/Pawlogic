# main.py
# Programa principal. Se ejecuta con: python src/main.py

from collections import Counter
from datetime import datetime, timedelta
import archivos
import auth
import config
import radicado
import reportes
import validaciones as val

LINEA = "-" * 60


class Cancelado(Exception):
    """Se usa cuando la persona escribe 'cancelar' en medio de un formulario."""


def pedir(mensaje, validador, opcional=False):
    while True:
        texto = input(f"  {mensaje}: ")
        if texto.strip().lower() == "cancelar":
            raise Cancelado()
        if opcional and texto.strip() == "":
            return validador("")
        try:
            return validador(texto)
        except ValueError as error:
            print(f"    X {error}")


def elegir(titulo, opciones):
    print(f"\n  {titulo}")
    for numero, opcion in enumerate(opciones, 1):
        print(f"    {numero}. {opcion}")
    return pedir("Opción", lambda texto: val.validar_opcion(texto, opciones))


def confirmar(pregunta):
    return input(f"  {pregunta} (s/n): ").strip().lower() in ("s", "si", "sí")


def elegir_tipo(titulo):
    etiquetas = list(config.ETIQUETAS_TIPO.values())
    etiqueta = elegir(titulo, etiquetas)
    return [clave for clave, nombre in config.ETIQUETAS_TIPO.items() if nombre == etiqueta][0]


def pedir_id(tipo):
    maximo = archivos.ultimo_id(tipo)

    def validar_id(texto):
        if not texto.strip().isdigit() or not 1 <= int(texto) <= maximo:
            raise ValueError(f"Escriba un ID entre 1 y {maximo}.")
        return int(texto)

    return pedir(f"ID (1 a {maximo})", validar_id)


def registrar_pqrs(sesion):
    print(f"\n{LINEA}\n  REGISTRAR PQRS   (escriba 'cancelar' para abortar)\n{LINEA}")
    activos = auth.usuarios_activos(archivos.leer_usuarios())
    if sesion["usuario"] not in activos:
        print("  X El usuario de la sesión no está autorizado.")
        return

    tipo = elegir_tipo("Tipo de solicitud:")
    print(f"\n  Será el ID {archivos.siguiente_id(tipo)} de {config.ETIQUETAS_TIPO[tipo]}.")

    print("\n  -- Datos del solicitante --")
    nombre = pedir("Nombre completo", val.validar_nombre)
    tipo_documento = elegir("Tipo de documento:", list(config.TIPOS_DOCUMENTO))
    numero_documento = pedir("Número de documento (3 a 15 dígitos)", val.validar_numero_documento)
    tipo_telefono = elegir("Tipo de teléfono:", config.TIPOS_TELEFONO)
    telefono = pedir("Teléfono de contacto (10 dígitos)", val.validar_telefono)
    correo = pedir("Correo electrónico", val.validar_correo)
    direccion = pedir("Dirección (Enter para omitir)", val.validar_direccion, opcional=True)

    print("\n  -- Información de la PQRS --")
    canal = elegir("Canal de recepción:", config.CANALES)
    fecha = pedir("Fecha de radicación (Enter = ahora, o AAAA-MM-DD HH:MM:SS)",
                  lambda texto: val.validar_fecha(texto) if texto.strip()
                  else datetime.now().replace(microsecond=0))
    asunto = pedir("Asunto o título (5 a 150 caracteres)", val.validar_asunto)
    descripcion = pedir("Descripción detallada (mínimo 20 caracteres)", val.validar_descripcion)

    print("\n  -- Información relacionada --")
    mascota = elegir("Tipo de mascota:", config.TIPOS_MASCOTA)
    campus = elegir("Campus relacionado:", config.CAMPUS)

    fecha_maxima = fecha + timedelta(days=config.PLAZO_DIAS)
    datos = {
        "nombre_completo": nombre,
        "tipo_documento": config.TIPOS_DOCUMENTO[tipo_documento],
        "numero_documento": numero_documento,
        "tipo_telefono": tipo_telefono,
        "telefono_contacto": telefono,
        "correo_electronico": correo,
        "direccion": direccion,
        "fecha_radicacion": fecha.strftime(config.FORMATO_FECHA),
        "canal_recepcion": canal,
        "asunto_titulo": asunto,
        "descripcion_detallada": descripcion,
        "tipo_mascota": mascota,
        "campus_relacionado": campus,
        "fecha_maxima_respuesta": fecha_maxima.strftime(config.FORMATO_FECHA),
        "estado_peticion": config.ESTADOS[0],
        "usuario_registro": sesion["usuario"],
    }
    print(f"\n  Fecha máxima de respuesta: {datos['fecha_maxima_respuesta']}")
    print(f"  Registrado por: {sesion['usuario']}")
    if not confirmar("¿Guardar esta PQRS?"):
        print("  Registro descartado.")
        return

    registro = archivos.guardar_registro(tipo, datos)
    ruta = radicado.guardar_radicado(registro)
    print(f"\n  PQRS guardada con ID {registro['id']} en {archivos.ruta_archivo(tipo).name}.")
    print(f"  Radicado guardado en: {ruta}\n")
    print(radicado.generar_radicado(registro))


def consultar_pqrs():
    print(f"\n{LINEA}\n  CONSULTAR PQRS\n{LINEA}")
    opcion = elegir("¿Qué desea consultar?", ["Una PQRS (ver su radicado)", "Estado general de las PQRS"])
    if opcion.startswith("Estado"):
        print(f"\n  {'Tipo':<12}{'Total':>7}" + "".join(f"{estado:>13}" for estado in config.ESTADOS))
        for tipo in config.ARCHIVOS_PQRS:
            registros = archivos.leer_registros(tipo)
            conteo = Counter(r["estado_peticion"] for r in registros)
            print(f"  {config.ETIQUETAS_TIPO[tipo]:<12}{len(registros):>7}"
                  + "".join(f"{conteo[estado]:>13}" for estado in config.ESTADOS))
        return
    tipo = elegir_tipo("Tipo de solicitud:")
    registro = archivos.buscar_registro(tipo, pedir_id(tipo))
    print()
    print(radicado.generar_radicado(registro) if registro else "  No se encontró el registro.")


def registrar_cambio():
    print(f"\n{LINEA}\n  REGISTRAR CAMBIO EN PQRS\n{LINEA}")
    tipo = elegir_tipo("Tipo de solicitud:")
    id_registro = pedir_id(tipo)
    registro = archivos.buscar_registro(tipo, id_registro)
    if registro is None:
        print("  No se encontró el registro.")
        return
    actual = registro["estado_peticion"]
    print(f"\n  {radicado.numero_radicado(tipo, id_registro)} - estado actual: {actual}")
    if actual == config.ESTADOS[-1]:
        print("  Ya está Solucionada; no admite más cambios.")
        return
    nuevo = config.ESTADOS[config.ESTADOS.index(actual) + 1]
    val.validar_cambio_estado(actual, nuevo)
    if confirmar(f"¿Cambiar de '{actual}' a '{nuevo}'?"):
        archivos.actualizar_estado(tipo, id_registro, nuevo)
        print(f"  Estado actualizado a '{nuevo}'.")


def menu_estadisticas():
    while True:
        print(f"\n{LINEA}\n  ESTADÍSTICAS\n{LINEA}")
        print("  1. Ver estadísticas en pantalla")
        print("  2. Exportar el reporte a un archivo de texto")
        print("  3. Exportar datos consolidados (.csv)")
        print("  4. Generar gráficos (se guardan en la carpeta images)")
        print("  5. Volver")
        opcion = input("\n  Seleccione una opción: ").strip()
        if opcion == "1":
            print(reportes.construir_reporte())
        elif opcion == "2":
            print(f"\n  Reporte guardado en: {reportes.exportar_reporte(reportes.construir_reporte())}")
        elif opcion == "3":
            ruta, total = reportes.exportar_consolidado()
            print(f"\n  {total} registros guardados en: {ruta}")
        elif opcion == "4":
            for ruta in reportes.generar_graficos():
                print(f"  Gráfico guardado: {ruta}")
        elif opcion == "5":
            return
        else:
            print("  Opción no válida.")


def menu_principal(sesion):
    while True:
        print(f"\n{'=' * 60}\n  Bienvenido a {config.NOMBRE_SISTEMA}")
        print(f"  Sesión: {sesion['nombre']} ({sesion['rol']})\n{'=' * 60}")
        print("    1. Registrar PQRS")
        print("    2. Consultar PQRS")
        print("    3. Registrar Cambio en PQRS")
        print("    4. Estadísticas")
        print("    5. Salir")
        opcion = input("\n  Seleccione una opción (1-5): ").strip()
        try:
            if opcion == "1":
                registrar_pqrs(sesion)
            elif opcion == "2":
                consultar_pqrs()
            elif opcion == "3":
                registrar_cambio()
            elif opcion == "4":
                menu_estadisticas()
            elif opcion == "5":
                return True
            else:
                print("  Opción no válida.")
        except Cancelado:
            print("\n  Operación cancelada.")
        except (OSError, ValueError) as error:
            print(f"\n  X Error: {error}")


def main():
    try:
        sesion = auth.iniciar_sesion()
        if sesion is not None:
            menu_principal(sesion)
    except (KeyboardInterrupt, EOFError):
        print()
    print("\n  Hasta pronto.")


if __name__ == "__main__":
    main()
