# Servicio de Asistencia

**Versión:** 1.0  
**Categoría:** Services  
**Autor:** Jesús Rincón  
**Licencia:** LGPL-3  

---

## Índice

1. [Descripción](#descripción)  
2. [Justificación de decisiones técnicas](#justificación-de-decisiones-técnicas)  
3. [Dificultades encontradas y soluciones](#dificultades-encontradas-y-soluciones)  
4. [Lecciones aprendidas y mejoras futuras](#lecciones-aprendidas-y-mejoras-futuras)  
5. [Tiempo invertido por sección](#tiempo-invertido-por-sección)  
6. [Referencias técnicas consultadas](#referencias-técnicas-consultadas)  

---

## Descripción

Este módulo de Odoo permite gestionar **servicios de asistencia** (soporte vial, médico y del hogar) integrando:

- Pantallas Kanban y Calendario para seguimiento por estado y fecha.  
- Integraciones a APIs simuladas de TRM y Tiempo de Atención.  
- Generación de reportes PDF personalizados.  
- Notificaciones por email y en el chatter de Odoo.  
- Control de acceso por grupos de usuario.  

---

## Demostración en video

Para ver un recorrido completo del funcionamiento y las principales características del módulo, revisa este video explicativo:

[▶️ Ver demostración en YouTube](https://youtu.be/JYkrosqJdhs)

[▶️ TRM](https://youtu.be/GQqtpujVCoA)

---

## Justificación de decisiones técnicas

- **Estructura estándar de módulo Odoo**  - MODELO MVC
  - (`__manifest__.py`, carpetas `models/`, `views/`, `reports/`, `data/`, `security/`)  
  - Facilita la instalación, actualización y mantenimiento según convenciones de la comunidad.

- **ORM de Odoo para modelos (`models/servicio_asistencia.py`)**  
  - Aprovecha herencia de `mail.thread` para chatter, reglas de acceso.

- **Integración de APIs en `api_integration.py`**  
  - Se creó un modelo `api.integration` para abstraer endpoints.  
  - La acción `action_consultar_api` delega llamadas a un servicio central, facilitando futuros cambios.

- **Generación de PDF con QWeb Reports**  
  - Plantillas QWeb (`report_template.xml`) permiten maquetar un informe adaptable a branding.  
  - Criterio: mantener estilo limpio, reutilizar fragmentos de vista.

- **Notificaciones en Chatter y Email**  
  - Uso de plantilla XML (`email_template.xml`) para emails.  
  - Mensajes en chatter con `message_post` para historial interno.

- **Herramientas y librerías**  
  - Odoo 17, Python 3.11.  
  - Dependencia externa: **wkhtmltopdf** para renderizar PDF (ver sección dificultades).

---

## Dificultades encontradas y soluciones

| Problema                                                           | Causa                                               | Solución aplicada                                                                                                   |
|--------------------------------------------------------------------|-----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Los PDF salían en blanco                                           | Librería `wkhtmltopdf` con una versión incompatible | Instalación de la versión recomendada por Odoo y configuración en `odoo.conf`  |
| Publicar mensajes al chatter desde código                          | No conocía la sintaxis exacta para Odoo 17          | Consulté la guía de Cybrosys y usé `record.message_post(body=…)`  |
| Obtener timestamp actual en Python                                 | Necesidad de convertir la fecha                     | Uso de `datetime.now().timestamp()` tras revisar ejemplo en GeeksforGeeks  |

---

## Lecciones aprendidas y mejoras futuras

- **Aprendizaje de QWeb y wkhtmltopdf** me permitió dominar reportes complejos.  
- Con más tiempo, incorporaría:  
  - Mejora en la tarjeta de creación en vista KANBAN
  - Mejora en el diseño de las plantillas de correo y PDF de acuerdo a los lineamientos del manual de identidad de marca
  - Control de errores para evitar que hayan contactos duplicados con el mismo correo (CRM y Módulo de asistencias)
  - Cuando se suba por plantilla CSV al módulo de CRM permitir nombres personalizados para la oportunidad
    - Ejm: Oportunidad + Tipo + Nombre del Usuario
  - Acción automatizada para consultar la TRM a diario
---

## Tiempo invertido por sección

| Sección                                                         | Horas estimadas |
|-----------------------------------------------------------------|-----------------|
| Planificación y diseño                                          | 1 h             |
| Modelado de datos y seguridad,Vistas (Kanban, Form, Calendario) | 1 h             |
| Reportes PDF y plantillas QWeb                                  | 2 h             |
| Notificaciones (email & chatter)                                | 1 h             |
| Integración de APIs                                             | 1 h             |            
| Documentación + Videos                                          | 1 h             |
| **Total aproximado**                                            | **7 h**         |

---

## Referencias técnicas consultadas

- Documentación oficial de **Odoo 17**  
- Stack Overflow y foros de Odoo  
- [Cómo publicar en chatter en Odoo 17 – Cybrosys](https://www.cybrosys.com/blog/how-to-post-a-message-to-chatter-in-odoo-17)
- [GeeksforGeeks: timestamp en Python](https://www.geeksforgeeks.org/python/get-current-timestamp-using-python/ )
- [Solución wkhtmltopdf en Odoo 17 – foro oficia](https://www.odoo.com/es/forum/ayuda-1/wkhtmltopdf-odoo-17-no-logo-or-footer-247715)
- [How to Add a Chatter in Odoo 17 | Adding a Chatter in Odoo 17 | Odoo 17 Development Tutorials](https://www.youtube.com/watch?v=qsJDZY6ojqQ)

---

