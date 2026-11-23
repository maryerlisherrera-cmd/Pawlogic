# config.py
# Aquí van los datos fijos del programa. Si algo cambia (por ejemplo el plazo),
# se cambia en UN solo lugar y todo el programa se actualiza.

from pathlib import Path

# --- Carpetas ---
# Path(__file__) es la ubicación de este archivo (src/config.py).
# .parent.parent sube dos niveles: llega a la carpeta principal del proyecto.
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATA = CARPETA_PROYECTO / "data"

# --- Reglas del programa ---
PLAZO_DIAS = 30            # días que tiene cada PQRS para ser respondida
MAX_INTENTOS = 3           # intentos de login antes de bloquear
SEGUNDOS_BLOQUEO = 30      # tiempo de bloqueo (se muestra en pantalla)
ANCHO_RADICADO = 120       # ancho exacto de cada línea del radicado
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
SEPARADOR = "|"            # separa las columnas dentro de los archivos .txt

# --- Archivos de datos ---
ARCHIVO_USUARIOS = "Usuarios.txt"
# tipo de solicitud -> nombre del archivo donde se guarda
ARCHIVOS_PQRS = {
    "Peticion": "Peticion.txt",
    "Queja": "Queja.txt",
    "Reclamo": "Reclamo.txt",
    "Sugerencia": "Sugerencia.txt",
}

# --- Opciones permitidas ---
TIPOS_DOCUMENTO = {
    "Cédula de ciudadanía": "CC",
    "Tarjeta de identidad": "TI",
    "Cédula de extranjería": "CE",
    "Pasaporte": "PP",
    "NIT": "NIT",
}
TIPOS_TELEFONO = ["Celular", "Fijo", "Corporativo", "Otro"]
CANALES = ["Presencial", "Correo electrónico", "Página web", "Teléfono", "Redes sociales", "Otro"]
TIPOS_MASCOTA = ["Perro", "Gato", "Otro"]
CAMPUS = [
    "Campus Medellín - Ciudad Universitaria",
    "Campus Medellín - Ciudadela Robledo",
    "Campus en el Área de la salud",
    "Campus Medellín - Sede de Posgrado",
    "Campus Medellín - Edificio San Ignacio",
    "Campus Medellín - Antigua Escuela de Derecho",
    "Campus Medellín - Edificio Antioquia",
    "Campus Medellín - Casas Patrimoniales",
    "Campus Medellín - Edificio de Extensión",
]
ESTADOS = ["Registrada", "En proceso", "Solucionada"]   # siempre en este orden

# --- Datos para el radicado y los reportes ---
NOMBRE_SISTEMA = "PAWLOGIC - Gestor de PQRS"
INSTITUCION = "MEPEGA - Movimiento Estudiantil de Perritos y Gaticos - Universidad de Antioquia"
CARPETA_RADICADOS = CARPETA_DATA / "radicados"
DIAS_ALERTA = 7            # una PQRS está "próxima a vencer" si le faltan menos de estos días
ARCHIVO_REPORTE = "reporte_estadisticas.txt"
ARCHIVO_CONSOLIDADO = "consolidado_pqrs.csv"

# Orden exacto de las 18 columnas de los archivos (igual que las bases del profe)
CAMPOS = [
    "id", "nombre_completo", "tipo_documento", "numero_documento", "tipo_telefono",
    "telefono_contacto", "correo_electronico", "direccion", "tipo_solicitud",
    "fecha_radicacion", "canal_recepcion", "asunto_titulo", "descripcion_detallada",
    "tipo_mascota", "campus_relacionado", "fecha_maxima_respuesta", "estado_peticion",
    "usuario_registro",
]
# tipo de solicitud -> prefijo del radicado y nombre con tilde para mostrar
PREFIJOS = {"Peticion": "PET", "Queja": "QUE", "Reclamo": "REC", "Sugerencia": "SUG"}
ETIQUETAS_TIPO = {"Peticion": "Petición", "Queja": "Queja", "Reclamo": "Reclamo", "Sugerencia": "Sugerencia"}

# --- Carpeta de los gráficos ---
CARPETA_IMAGES = CARPETA_PROYECTO / "images"