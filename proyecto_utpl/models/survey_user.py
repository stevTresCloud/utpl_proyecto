# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.model
    def create(self, vals):
        res = super(SurveyUserInput, self).create(vals)
        # if 'partner_id' in vals:
        return res

    def write(self, vals):
        res = super(SurveyUserInput, self).write(vals)
        return res
