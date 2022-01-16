# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime, date
from monthdelta import monthdelta
from dateutil import rrule
from odoo.exceptions import UserError, ValidationError

TYPE_PERIOD_NUMBER = {
    'bimonthly': 2,
    'trimonthly': 3,
    'quarterly': 4,
    'quimestral': 5,
    'semester': 6,
}


class CareerPeriod(models.Model):
    _name = 'career.period'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Periodo Lectivo'

    @api.model
    def default_get(self, fields):
        res = super(CareerPeriod, self).default_get(fields)
        if res.get('type_period', False) and not res.get('date_end', False):
            res['date_end'] = datetime.today() + monthdelta(TYPE_PERIOD_NUMBER[res.get('type_period')])
        return res

    @api.constrains('date_end', 'day_trip', 'type_period')
    def _check_career_period_dates(self):
        month_count = rrule.rrule(rrule.MONTHLY, dtstart=self.date_begin, until=self.date_end).count()
        if month_count < TYPE_PERIOD_NUMBER[self.type_period] or month_count > TYPE_PERIOD_NUMBER[self.type_period]:
            raise ValidationError(u'Las fechas del periodo lectivo, no cumplen con los meses de distancia (%s) que se calculan a partir de la fecha de inicio y fin del periodo lectivo. Revise nuevamente antes de guardar el registro.' % month_count)

    name = fields.Char(
        'Nombre del periodo',
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
    type_period = fields.Selection(
        [('bimonthly', 'Bimestral'),
         ('trimonthly', 'Trimestral'),
         ('quarterly', 'Cuatrimestral'),
         ('quimestral', 'Quimestral'),
         ('semester', 'Semestre')],
        string='Tipo de periodo',
        default='semester',
        required=True,
    )
    date_begin = fields.Datetime(
        string='Fecha de inicio',
        required=True,
        tracking=True,
        default=datetime.today(),
    )
    date_end = fields.Datetime(
        string='Fecha de finalización',
        required=True,
        tracking=True,
    )
    day_trip = fields.Many2one(
        'day.trip',
        string='Jornada',
        help='Jornada del periodo lectivo',
        required=True,
    )
    description = fields.Char(
        string=u'Descripción',
        help=u'Descripción del periodo lectivo'
    )
