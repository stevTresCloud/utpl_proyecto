# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    property_default_minimum_score_to_pass = fields.Float(
        'Puntaje por defecto mínimo para aprobar',
        help='Puntaje por defecto mínimo para aprobar',
        default=7.0,
    )
