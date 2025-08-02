from odoo import models, fields, api, _
import base64, logging

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
    fecha_solicitud = fields.Datetime(string='Fecha de Solicitud', required=True,default=fields.Datetime.now)
    ESTADOS = [
        ('pendiente',    'Pendiente'),
        ('en_proceso',   'En Proceso'),
        ('finalizado',   'Finalizado'),
    ]
    estado = fields.Selection(
        selection=ESTADOS,
        string='Estado',
        required=True,              # evita valores en blanco
        default='pendiente',        # todos los nuevos serán 'Pendiente'
        group_expand='_expand_estados',
    )
    descripcion = fields.Text(string='Descripción')
    costo_estimado = fields.Float(string='Costo Estimado')

    def action_generar_pdf(self):
        return self.env.ref('asisya_servicios_asistencia.action_report_asistencia_pdf').report_action(self)

    @api.model
    def _expand_estados(self, states, domain, order):
        return [key for key, _ in self.ESTADOS]

    @api.onchange('estado')
    def _onchange_estado(self):
        # Sólo al pasar a finalizado
        if self.estado == 'finalizado':
            self.action_generar_pdf()

    @api.model
    def create(self, vals):
        record = super(ServicioAsistencia, self).create(vals)
        if record.cliente_id.email:
            template = self.env.ref(
                'asisya_servicios_asistencia.email_template_asistencia'
            )
            # 1) Enviar el correo al cliente
            template.send_mail(record.id, force_send=True)
        return record

    def write(self, vals):
        res = super().write(vals)
        if vals.get('estado') == 'finalizado':
            report_obj = self.env['ir.actions.report']
            xmlid = 'asisya_servicios_asistencia.action_report_asistencia_pdf'
            for rec in self:
                _logger.info(f"Asistencia {rec.id} -> finalizado, genero y adjunto PDF")
                pdf_bytes, _ = report_obj._render_qweb_pdf(xmlid, [rec.id])
                attachment = self.env['ir.attachment'].create({
                    'name':       f'Asistencia_{rec.cliente_id.name}.pdf',
                    'type':       'binary',
                    'datas':      base64.b64encode(pdf_bytes),
                    'res_model':  rec._name,
                    'res_id':     rec.id,
                    'mimetype':   'application/pdf',
                })
                rec.message_post(
                    body="PDF de finalización generado automáticamente.",
                    attachment_ids=[attachment.id],
                )
        return res