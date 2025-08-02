{
    'name': 'Servicio de Asistencia',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestión de asistencias y consultas a APIs externas simuladas',
    'description': """
        Módulo para gestionar servicios de asistencia como soporte vial, médico y del hogar.
        Funcionalidades:
        - Registro y seguimiento de asistencias por estado.
        - Integración con APIs simuladas (TRM y Tiempo de Atención).
        - Vista Kanban para gestión visual por estado.
        - Vista calendario por fecha de solicitud.
        - Reporte PDF detallado.
        - Control de acceso por grupos (Interno y Gerente).
    """,
    'author': 'Jesus Rincon',
    'website': 'https://www.linkedin.com/in/jesussebastian/',
    'icon': 'asisya_servicios_asistencia/static/description/icon.png',
    'depends': ['base', 'web', 'mail','crm'],
    'data': [
        'security/servicio_asistencia_groups.xml',
        'security/ir.model.access.csv',
        'views/servicio_asistencia_views.xml',
        'views/menus.xml',
        'views/crm_lead_views.xml',
        'reports/report.xml',
        'reports/report_template.xml',
        'data/email_template.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}