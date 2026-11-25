# Manual de Usuario – Pawlogic (Gestor de PQRS MEPEGA)

## 1. Requisitos del sistema
- Python 3.10 o superior instalado.
- Librerías externas: `pandas` y `matplotlib` (instalables con `pip install -r requirements.txt`).

## 2. Ejecución del programa
1. Abrir la terminal en la carpeta raíz del proyecto (`Pawlogic`).
2. Ejecutar el comando:
   ```bash
   python src/main.py

   ## 3. Inicio de sesión (Login)
- Al iniciar, el sistema solicita **Usuario** y **Contraseña** registrados en `data/Usuarios.txt` (ejemplo: `admin_udea`).
- Por seguridad, si se ingresan credenciales incorrectas **3 veces seguidas**, el sistema bloquea temporalmente el acceso y muestra el tiempo de espera en pantalla.
- Una vez autenticado, el usuario queda vinculado automáticamente a todas las PQRS que registre en esa sesión.

## 4. Menú Principal y Operaciones
1. **Registrar PQRS:**
   - Solicita los datos del ciudadano (nombre, tipo y número de documento, teléfono, correo y dirección opcional) y los detalles de la solicitud (tipo: Petición, Queja, Reclamo o Sugerencia; canal, asunto, descripción, tipo de mascota y campus UdeA).
   - Valida cada campo antes de guardar y asigna un **ID consecutivo independiente** en el archivo plano correspondiente (`data/Peticion.txt`, `data/Queja.txt`, `data/Reclamo.txt` o `data/Sugerencia.txt`), calculando la fecha máxima de respuesta (+30 días calendario).
   - Genera e imprime en consola y archivo el **comprobante de radicado ASCII de 120 caracteres de ancho**.
2. **Consultar PQRS:**
   - Permite buscar solicitudes registradas por ID o criterios de filtro y visualizar su ficha completa.
3. **Registrar Cambio en PQRS:**
   - Permite actualizar el estado siguiendo el flujo obligatorio: `Registrada` → `En proceso` → `Solucionada`.
   - Al pasar a `Solucionada`, registra la fecha de respuesta y calcula los días transcurridos.
4. **Estadísticas:**
   - Calcula el promedio de días de respuesta (en enteros) y genera en la carpeta `images/` las gráficas estadísticas por tipo de mascota, canal de recepción, campus UdeA, estado de resolución y usuarios registradores.
5. **Salir:**
   - Cierra de forma segura la sesión del sistema.