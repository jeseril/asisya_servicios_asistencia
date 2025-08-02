from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)

class ServicioAsistencia(models.Model):
    _name = 'servicio.asistencia'
    _description = 'Registro de Servicio de Asistencia'
    _inherit = ['mail.thread']

    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    tipo_asistencia = fields.Selection([
        ('vial', 'Vial'),
        ('medica', 'Médica'),
        ('hogar', 'Hogar')
    ], string='Tipo de Asistencia', required=True)
    ubicacion = fields.Char(string='Ubicación', required=True)
    fecha_solicitud = fields.Datetime(string='Fecha de Solicitud', default=fields.Datetime.now)
    estado = fields.Selection([
        ('solicitado', 'Solicitado'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado')
    ], string='Estado', default='solicitado', tracking=True)
    descripcion = fields.Text(string='Descripción')
    costo_estimado = fields.Float(string='Costo Estimado')
