# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = "res.users"

    @api.depends('compute_user_type')
    def _compute_user_type(self):
        for user in self:
            if user.has_group('base.group_user'):
                user.compute_user_type = self.env.ref('base.group_user')
            elif user.has_group('base.group_portal'):
                user.compute_user_type = self.env.ref('base.group_portal')
            elif user.has_group('base.group_public'):
                user.compute_user_type = self.env.ref('base.group_public')
            else:
                user.compute_user_type = False

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

    compute_user_type = fields.Many2one(
        'res.groups',
        string='Tipo de usuario',
        help='Tipo de usuario',
        compute='_compute_user_type',
        store=True,
        copy=False
    )
