# coding: utf-8

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    property_default_minimum_score_to_pass = fields.Float(
        related='company_id.property_default_minimum_score_to_pass',
        readonly=False,
    )
