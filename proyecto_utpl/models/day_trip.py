# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class DayTrip(models.Model):
    _name = 'day.trip'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'modalidad o modalidad en la que la carrera será configurada.'

    @api.constrains('time_begin', 'time_end')
    def _check_day_trip_time(self):
        if self.time_end <= self.time_begin:
            raise ValidationError(u'La hora de finalización debe ser mayor que la fecha de inicio. vuelva a digitar las horas correctas')

    name = fields.Char(
        string=u'Nombre de la modalidad',
        help=u'Modalidad',
        required=True,
    )
    active = fields.Boolean('Estado', default=True)
    sequence = fields.Integer('Secuencia', default=10)
    time_begin = fields.Float(
        'Hora de inicio',
        required=True,
        help='Hora de inicio de la modalidad'
    )
    time_end = fields.Float(
        'Hora de finalización',
        required=True,
        help='Hora de finalización de la modalidad'
    )
    time_day = fields.Selection(
        [('morning', 'Mañana'),
         ('evening', 'Tarde')],
        string='modalidad',
        required=True,
        help='modalidad en la que se matriculará al estudiante',
        default='morning',
    )
    description = fields.Text(
        string=u'Descripción',
        help=u'Descripción de la carrera.'
    )
