# reportes.py
# Estadísticas de las PQRS usando PANDAS (cálculos) y MATPLOTLIB (gráficos).
# La PRIMERA estadística (obligatoria) es el promedio de días de respuesta.
# También exporta el reporte a un archivo de texto y un archivo consolidado para Power BI.

import csv
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")                # guarda los gráficos como imagen, sin abrir ventanas
import matplotlib.pyplot as plt
import pandas as pd

import config


def cargar_todos():
    """Lee los 4 archivos con pandas y los junta en UNA tabla (DataFrame)."""
    tablas = []
    for nombre_archivo in config.ARCHIVOS_PQRS.values():
        ruta = config.CARPETA_DATA / nombre_archivo
        tablas.append(pd.read_csv(ruta, sep=config.SEPARADOR, dtype=str, encoding="utf-8-sig",
                                  quoting=csv.QUOTE_NONE, keep_default_na=False))
    tabla = pd.concat(tablas, ignore_index=True)
    # Las fechas llegan como texto: se convierten a fecha para poder restarlas y compararlas.
    tabla["fecha_radicacion"] = pd.to_datetime(tabla["fecha_radicacion"], format=config.FORMATO_FECHA)
    tabla["fecha_maxima_respuesta"] = pd.to_datetime(tabla["fecha_maxima_respuesta"], format=config.FORMATO_FECHA)
    return tabla


def contar(tabla, columna):
    """Cuenta cuántas PQRS hay por cada valor de una columna. Devuelve (valor, cantidad, porcentaje)."""
    cantidades = tabla[columna].value_counts()                  # de mayor a menor
    porcentajes = (cantidades * 100 / len(tabla)).round(1)
    return [(valor, int(cantidades[valor]), float(porcentajes[valor])) for valor in cantidades.index]


def promedio_dias_respuesta(tabla, hoy):
    """ESTADÍSTICA OBLIGATORIA: promedio de días (entero) que toma dar respuesta.
    OJO: las bases del profe NO traen la fecha en que se respondió cada PQRS.
    Mientras él define cómo calcularlo, se usa: días desde la radicación hasta hoy,
    solo para las PQRS en estado 'Solucionada'."""
    solucionadas = tabla[tabla["estado_peticion"] == "Solucionada"]
    if solucionadas.empty:
        return None
    dias = (hoy - solucionadas["fecha_radicacion"]).dt.days
    return round(dias.mean())


def alertas_vencimiento(tabla, hoy):
    """Separa las PQRS NO solucionadas en: vencidas y próximas a vencer (menos de DIAS_ALERTA días)."""
    pendientes = tabla[tabla["estado_peticion"] != "Solucionada"]
    limite = hoy + timedelta(days=config.DIAS_ALERTA)
    fecha_maxima = pendientes["fecha_maxima_respuesta"]
    vencidas = pendientes[fecha_maxima < hoy]
    por_vencer = pendientes[(fecha_maxima >= hoy) & (fecha_maxima <= limite)]
    return pendientes, vencidas, por_vencer


def mas_antiguas(tabla, cantidad=5):
    """Las PQRS sin solucionar con la fecha de radicación más vieja (lista de diccionarios)."""
    pendientes = tabla[tabla["estado_peticion"] != "Solucionada"]
    return pendientes.sort_values("fecha_radicacion").head(cantidad).to_dict("records")


def _tabla(titulo, filas):
    """Convierte [(valor, cantidad, porcentaje)] en líneas de texto."""
    lineas = [titulo]
    lineas += [f"    {valor:<48} {cantidad:>6}  ({porcentaje}%)" for valor, cantidad, porcentaje in filas]
    return lineas


def construir_reporte(tabla=None, hoy=None):
    """Arma el reporte completo como texto."""
    tabla = cargar_todos() if tabla is None else tabla
    hoy = hoy or datetime.now()
    total = len(tabla)
    promedio = promedio_dias_respuesta(tabla, hoy)
    pendientes, vencidas, por_vencer = alertas_vencimiento(tabla, hoy)

    lineas = [
        "=" * 70,
        f"  ESTADÍSTICAS DE PQRS  -  generado el {hoy.strftime(config.FORMATO_FECHA)}",
        "=" * 70,
        f"Total de PQRS registradas: {total}",
        "",
        "1. PROMEDIO DE DÍAS DE RESPUESTA (estadística obligatoria)",
        f"    {promedio} días" if promedio is not None else "    Sin PQRS solucionadas.",
        "    (Nota: se calcula con la antigüedad de las solucionadas; las bases no traen fecha de respuesta.)",
        "",
        *_tabla("2. SOLICITUDES POR TIPO DE MASCOTA", contar(tabla, "tipo_mascota")),
        "",
        *_tabla("3. PROPORCIÓN POR CANAL DE RECEPCIÓN", contar(tabla, "canal_recepcion")),
        "",
        *_tabla("4. DISTRIBUCIÓN POR CAMPUS", contar(tabla, "campus_relacionado")),
        "",
        *_tabla("5. EFECTIVIDAD: PQRS POR ESTADO", contar(tabla, "estado_peticion")),
        "",
        "6. ALERTAS DE VENCIMIENTO (PQRS sin solucionar)",
        f"    Sin solucionar:                       {len(pendientes):>6}",
        f"    Vencidas (pasó la fecha máxima):      {len(vencidas):>6}  ({round(len(vencidas) * 100 / total, 1)}% del total)",
        f"    Próximas a vencer (menos de {config.DIAS_ALERTA} días): {len(por_vencer):>6}  ({round(len(por_vencer) * 100 / total, 1)}% del total)",
        "",
        *_tabla("7. PQRS POR TIPO DE SOLICITUD",
                [(config.ETIQUETAS_TIPO[v], c, p) for v, c, p in contar(tabla, "tipo_solicitud")]),
        "",
        *_tabla("8. CARGA OPERATIVA: PQRS REGISTRADAS POR USUARIO", contar(tabla, "usuario_registro")),
        "    Perfil del solicitante (Estudiante, Docente...): PENDIENTE, las bases no traen ese dato.",
        "",
        "9. LAS 5 PQRS MÁS ANTIGUAS SIN SOLUCIONAR",
    ]
    lineas += [f"    {config.ETIQUETAS_TIPO[r['tipo_solicitud']]:<11} ID {r['id']:>5}   "
               f"radicada {r['fecha_radicacion'].strftime(config.FORMATO_FECHA)}   "
               f"vence {r['fecha_maxima_respuesta'].strftime(config.FORMATO_FECHA)}   [{r['estado_peticion']}]"
               for r in mas_antiguas(tabla)]
    lineas.append("")
    return "\n".join(lineas)


def exportar_reporte(texto):
    """Guarda el reporte en un archivo de texto (data/reporte_estadisticas.txt)."""
    ruta = config.CARPETA_DATA / config.ARCHIVO_REPORTE
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    return ruta


def exportar_consolidado():
    """Junta las 4 bases en UN archivo .csv, listo para abrirlo en Power BI."""
    tabla = cargar_todos()
    ruta = config.CARPETA_DATA / config.ARCHIVO_CONSOLIDADO
    tabla.to_csv(ruta, index=False, encoding="utf-8-sig", date_format=config.FORMATO_FECHA)
    return ruta, len(tabla)


# ------------------------------------------------------------------ gráficos (matplotlib)
def _guardar(figura, nombre):
    """Guarda la figura como imagen PNG en la carpeta images y la cierra."""
    config.CARPETA_IMAGES.mkdir(parents=True, exist_ok=True)
    ruta = config.CARPETA_IMAGES / nombre
    figura.tight_layout()
    figura.savefig(ruta, dpi=120)
    plt.close(figura)
    return ruta


def generar_graficos(tabla=None, hoy=None):
    """Crea 6 gráficos PNG en la carpeta images y devuelve la lista de rutas."""
    tabla = cargar_todos() if tabla is None else tabla
    hoy = hoy or datetime.now()
    rutas = []

    # 1. Torta: solicitudes por tipo de mascota
    datos = tabla["tipo_mascota"].value_counts()
    figura, eje = plt.subplots(figsize=(6, 6))
    eje.pie(datos.values, labels=datos.index, autopct="%1.1f%%", startangle=90)
    eje.set_title("Solicitudes por tipo de mascota")
    rutas.append(_guardar(figura, "grafico_mascota.png"))

    # 2. Barras: PQRS por canal de recepción
    datos = tabla["canal_recepcion"].value_counts()
    figura, eje = plt.subplots(figsize=(8, 5))
    eje.bar_label(eje.bar(datos.index, datos.values))
    eje.margins(y=0.1)
    eje.set_title("PQRS por canal de recepción")
    eje.set_ylabel("Cantidad")
    eje.tick_params(axis="x", rotation=30)
    rutas.append(_guardar(figura, "grafico_canal.png"))

    # 3. Barras horizontales: PQRS por campus
    datos = tabla["campus_relacionado"].value_counts().sort_values()
    figura, eje = plt.subplots(figsize=(10, 5))
    eje.bar_label(eje.barh(datos.index, datos.values))
    eje.margins(x=0.1)
    eje.set_title("PQRS por campus de la UdeA")
    eje.set_xlabel("Cantidad")
    rutas.append(_guardar(figura, "grafico_campus.png"))

    # 4. Barras: PQRS por estado (efectividad)
    datos = tabla["estado_peticion"].value_counts().reindex(config.ESTADOS)
    figura, eje = plt.subplots(figsize=(6, 5))
    eje.bar_label(eje.bar(datos.index, datos.values, color=["#f0ad4e", "#5bc0de", "#5cb85c"]))
    eje.margins(y=0.1)
    eje.set_title("PQRS por estado")
    eje.set_ylabel("Cantidad")
    rutas.append(_guardar(figura, "grafico_estado.png"))

    # 5. Barras: alertas de vencimiento
    pendientes, vencidas, por_vencer = alertas_vencimiento(tabla, hoy)
    nombres = ["Sin solucionar", "Vencidas", f"Por vencer (<{config.DIAS_ALERTA} días)"]
    valores = [len(pendientes), len(vencidas), len(por_vencer)]
    figura, eje = plt.subplots(figsize=(7, 5))
    eje.bar_label(eje.bar(nombres, valores, color=["#f0ad4e", "#d9534f", "#5bc0de"]))
    eje.margins(y=0.1)
    eje.set_title("Alertas de vencimiento")
    eje.set_ylabel("Cantidad")
    rutas.append(_guardar(figura, "grafico_vencimiento.png"))

    # 6. Barras horizontales: PQRS registradas por usuario
    datos = tabla["usuario_registro"].value_counts().sort_values()
    figura, eje = plt.subplots(figsize=(8, 6))
    eje.bar_label(eje.barh(datos.index, datos.values))
    eje.margins(x=0.1)
    eje.set_title("PQRS registradas por usuario")
    eje.set_xlabel("Cantidad")
    rutas.append(_guardar(figura, "grafico_usuarios.png"))

    return rutas


# Prueba rápida: SOLO corre al ejecutar este archivo (botón ▶). Muestra el reporte y crea los gráficos.
if __name__ == "__main__":
    print(construir_reporte())
    for ruta in generar_graficos():
        print("Gráfico guardado:", ruta)