from odoo import models, api, exceptions, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    asistencia_ids = fields.One2many(
        comodel_name='servicio.asistencia',
        inverse_name='cliente_id',
        string='Asistencias',
        compute='_compute_asistencias',
        readonly=True,
        copy=False,
    )

    #api.onchange, create y write me llevan a aquí para validar
    def _find_partner_by_email(self, email):
        #Método helper: busca y devuelve el partner que tenga ese email.
        return self.env['res.partner'].search([('email', '=', email)], limit=1)

    @api.onchange('email_from')
    def _onchange_email_from_assign_partner(self):
        if self.email_from:
            self.partner_id = self._find_partner_by_email(self.email_from)

    @api.model
    def create(self, vals):
        email = vals.get('email_from')
        if email:
            partner = self._find_partner_by_email(email)
            if partner:
                vals['partner_id'] = partner.id
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        # Si cambiaron email_from, reaplicamos la asignación en cada registro
        if 'email_from' in vals:
            for lead in self:
                if lead.email_from:
                    lead.partner_id = lead._find_partner_by_email(lead.email_from)
        return res

    @api.depends('partner_id')
    def _compute_asistencias(self):
        for lead in self:
            if lead.partner_id:
                lead.asistencia_ids = self.env['servicio.asistencia'].search([
                    ('cliente_id', '=', lead.partner_id.id)
                ])
            else:
                lead.asistencia_ids = [(5, 0, 0)]  # limpia la lista si no hay partner