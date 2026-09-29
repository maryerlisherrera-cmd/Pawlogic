# Pawlogic

![Logo de Pawlogic](images/logo.png)

**Pawlogic** es un gestor de PQRS (Peticiones, Quejas, Reclamos y Sugerencias) por consola, desarrollado en Python, que apoya al Movimiento Estudiantil de Perritos y Gaticos (MEPEGA) en la atención de perros y gatos en la Universidad de Antioquia.

## 1. Integrantes

| Nombre | Programa académico | Rol |
|--------|--------------------|-----|
| Maryerlis Herrera De Arcos | Ingeniería Industrial | Por definir |
| Valeria López Silva | Ingeniería Industrial | Por definir |
| Jehren Esther Padilla Villalba | Ingeniería Industrial | Por definir |
| Isabella Barros Correa | Ingeniería Industrial | Por definir |

## 2. Vínculos académicos y descripción

### Maryerlis Herrera de Arcos (líder del equipo)
- **Programa académico:** Ingeniería Industrial
- **Habilidades y fortalezas:** buena para exponer y comunicarse con claridad. Maneja Excel, lo que ayuda con la parte de estadísticas del proyecto.

### Isabella Barros Correa
- **Programa académico:** Ingeniería Industrial
- **Habilidades y fortalezas:** se le facilita hacer cuentas y maneja Excel, por lo que puede apoyar el presupuesto y los cálculos. Es puntual cuando su disponibilidad se lo permite.

### Valeria López Silva
- **Programa académico:** Ingeniería Industrial
- **Habilidades y fortalezas:** buena para organizar y redactar, lo que aporta a la documentación. Se defiende en Excel y se comunica bien.

### Jehren Esther Padilla Villalba
- **Programa académico:** Ingeniería Industrial
- **Habilidades y fortalezas:** se defiende en Excel, es puntual y expone bien.

## 3. Nombre del proyecto y detalles

**Nombre:** Pawlogic

**Significado:** unión de *Paw* (pata) y *Logic* (lógica). Representa un sistema ordenado y eficiente para gestionar la atención de perros y gatos.

**Descripción:** programa de consola que permite registrar PQRS con validación de datos, guardarlas en archivos planos independientes por tipo, generar un comprobante de radicado y consultar su estado. Reemplaza el registro manual en papel y lápiz que hoy usa MEPEGA.

**Logo:** ver la carpeta `images/` (pendiente).

## 4. Licencia del software

**Licencia elegida:** Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0).

**Enlace:** https://creativecommons.org/licenses/by-nc-sa/4.0/

**Justificación:**
- **Atribución (BY):** cualquier persona que use o adapte Pawlogic debe reconocer al equipo autor.
- **No comercial (NC):** el software se desarrolla con fines académicos y de apoyo a un movimiento estudiantil, por lo que no debe venderse.
- **Compartir igual (SA):** las versiones modificadas deben publicarse bajo esta misma licencia, para que el trabajo siga siendo abierto.

## 5. Reporte de visión

### Problema identificado

MEPEGA recibe PQRS (peticiones, quejas, reclamos y sugerencias) por varios medios: redes sociales, correo electrónico, papel y voz a voz. Hoy los estudiantes las procesan a papel y lápiz y les asignan a mano un número consecutivo. Esto genera riesgo de números repetidos o saltados, datos incompletos o mal escritos, dificultad para consultar el estado de cada solicitud y ningún control claro sobre el plazo máximo de respuesta de 30 días.

### Propuesta de valor

Pawlogic es un programa de consola que centraliza el registro de las PQRS. Valida cada dato antes de guardarlo, asigna automáticamente un radicado consecutivo y sin repetir, calcula la fecha máxima de respuesta, guarda cada tipo de solicitud en su propio archivo y entrega un comprobante impreso en texto. Además, exige iniciar sesión, de modo que cada registro queda asociado a quien lo ingresó.

### Objetivo general

Reemplazar el registro manual de PQRS de MEPEGA por un sistema en Python, ordenado y confiable, que apoye la atención de perros y gatos en la Universidad de Antioquia.

### Objetivos específicos

- Controlar el acceso al sistema con usuario y contraseña, con máximo 3 intentos y bloqueo temporal.
- Registrar las PQRS con validación estricta de los datos del solicitante y de la solicitud.
- Guardar cada tipo de PQRS en un archivo independiente, con su propio consecutivo.
- Generar un comprobante de radicado en texto, de 120 caracteres de ancho.
- Permitir consultar las PQRS y su estado, y calcular estadísticas para medir la atención.

### Beneficios

- **Orden:** consecutivos automáticos, sin números repetidos.
- **Calidad de los datos:** las validaciones evitan errores de digitación.
- **Control de tiempos:** cada PQRS tiene su fecha máxima de respuesta.
- **Trazabilidad:** se sabe qué usuario registró cada solicitud.
- **Ahorro de tiempo:** se reduce el trabajo a papel y lápiz.

### Alcance

**Incluye:** inicio de sesión, registro y validación de PQRS, almacenamiento en cuatro archivos planos, radicado en texto, consulta de estado y estadísticas.

**No incluye:** interfaz gráfica ni base de datos en servidor. Es un programa de consola que trabaja con archivos planos.

## 6. Especificación de requisitos

### Requisitos funcionales

Pendiente.

### Requisitos no funcionales

Pendiente.

## 7. Plan de proyecto

### Actividades y cronograma (Diagrama de Gantt)

Pendiente.

### Presupuesto

Pendiente.