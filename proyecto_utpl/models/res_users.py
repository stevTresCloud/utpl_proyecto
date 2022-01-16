# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    @api.onchange('type_partner')
    def _onchange_type_partner(self):
        group_portal = self.env.ref('base.group_portal')
        if group_portal.id not in self.groups_id.ids and self.type_partner == 'student':
            self.groups_id |= group_portal

    @api.onchange('groups_id')
    def _onchange_groups_id_probando(self):
        self.groups_id
