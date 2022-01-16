# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class DayTrip(models.Model):
    _name = 'day.trip'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Jornada'

    @api.constrains('time_begin', 'time_end')
    def _check_day_trip_time(self):
        if self.time_end <= self.time_begin:
            raise ValidationError(u'La hora de finalización debe ser mayor que la fecha de inicio. vuelva a digitar las horas correctas')

    # @api.depends('time_begin', 'time_end')
    # def _compute_day_trip_time(self):
    #     for trip in self:
    #         if self.time_begin

    name = fields.Char(
        string=u'Nombre de la jornada',
        help=u'Jornada',
        required=True,
    )
    active = fields.Boolean('Estado', default=True)
    sequence = fields.Integer('Secuencia', default=10)
    time_begin = fields.Float(
        'Hora de inicio',
        required=True,
        help='Hora de inicio de la jornada'
    )
    time_end = fields.Float(
        'Hora de finalización',
        required=True,
        help='Hora de finalización de la jornada'
    )
    time_day = fields.Selection(
        [('morning', 'Mañana'),
         ('evening', 'Tarde')],
        string='Jornada',
        required=True,
        help='Jornada en la que se matriculará al estudiante',
        default='morning',
        # compute='_compute_day_trip_time',
    )
    description = fields.Text(
        string=u'Descripción',
        help=u'Descripción de la carrera.'
    )
