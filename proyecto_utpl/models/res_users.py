# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        '''
        Al crear un registro, revisamos que si es de estudiante, sea de portal
        '''
        res = super(Users, self).create(vals)
        if res:
            res._check_type_partner()
        return res

    @api.constrains('type_partner')
    def _check_type_partner(self):
        '''
        Los usuarios de portal son solo estudiantes
        '''
        if self.env.ref('base.group_portal').id not in self.groups_id.ids and self.type_partner == 'student':
            raise ValidationError(u'Los usuarios tipo estudiantes, solo pueden ser usuarios de portal.')
