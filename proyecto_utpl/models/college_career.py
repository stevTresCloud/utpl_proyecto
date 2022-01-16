# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CollegeCareer(models.Model):
    _name = 'college.career'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Carrera'

    name = fields.Char(
        'Nombre de la carrera',
        required=True,
    )
    active = fields.Boolean(
        'Estado',
        default=True
    )
    sequence = fields.Integer(
        'Secuencia',
        default=10
    )
    description = fields.Char(
        string=u'Descripción',
        help=u'Descripción de la carrera.'
    )
    subjects_ids = fields.Many2many(
        'student.subject',
        string='Materias',
        help='Materias de la carrera.'
    )
