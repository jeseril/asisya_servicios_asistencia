from odoo import api, fields, models, _
import requests
import time
import logging

_logger = logging.getLogger(__name__)

class ApiIntegracion(models.Model):
    _name = 'api.integration'
    _description = 'Resultados de Integración con APIs Simuladas'

    asistencia_id = fields.Many2one(
        comodel_name='servicio.asistencia',
        string='Asistencia',
        required=True,
        ondelete='cascade',
    )
    trm = fields.Float(string='TRM (Simulada)')
    tiempo_atencion = fields.Integer(string='Tiempo Atención (min)')
    last_update = fields.Datetime(string='Última Actualización')
    state = fields.Selection([
        ('done', 'Éxito'),
        ('error', 'Error'),
        ('fallback', 'Fallback'),
    ], string='Estado', default='done')
    error_msg = fields.Text(string='Detalle de Error')
