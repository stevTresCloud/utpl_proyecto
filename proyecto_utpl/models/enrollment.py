# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, date


class Enrollment(models.Model):
    _name = 'enrollment'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Matrícula'

    @api.model
    def create(self, vals):
        return super(Enrollment, self).create(vals)

    def action_matriculate(self):
        if self.name == 'Borrador':
            self.name = self.classroom_id.sequence_id.next_by_id()
        self.student_partner_id.enrollment_id = self.id
        if not self.college_career_id.subjects_ids:
            raise ValidationError('Debe añadir al menos una materia en la carrera %s para matricular al estudiante %s.' % (self.college_career_id.name, self.student_partner_id.name))
        new_subjects_ids = self.env['student_subject.res_partner_rel']
        for subject in self.college_career_id.subjects_ids:
            new_subjects_ids += self.env['student_subject.res_partner_rel'].create({
                'subject_id': subject.id,
                'student_id': self.student_partner_id.id,
                'enrollment_id': self.id,
            })
        self.subjects_ids = new_subjects_ids
        self.write({'state': 'matriculate'})

    def action_cancel(self):
        if self.subjects_ids.mapped('subject_scores_ids'):
            raise ValidationError(u'No puede cancelar una matrícula porque el estudiante %s ya tiene materias con notas relaciondas.' % self.student_partner_id.name)
        self.student_partner_id.enrollment_id = False
        self.write({
            'subjects_ids': [(2, subject.id) for subject in self.subjects_ids]
        })
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    name = fields.Char(
        string=u'Matrícula',
        help=u'Nombre de la matrícula',
        readonly=True,
        store=True,
        default='Borrador'
    )
    state = fields.Selection(
        [('draft', 'Borrador'),
         ('matriculate', 'Matriculado'),
         ('cancel', 'Cancelado')],
        default='draft'
    )
    active = fields.Boolean('Estado', default=True)
    student_partner_id = fields.Many2one(
        'res.partner',
        string='Estudiante',
        help='Estudiante a matricular.',
        required=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)], 'cancel': [('readonly', True)]}
    )
    career_period_id = fields.Many2one(
        'career.period',
        string='Periodo Lectivo',
        required=True,
        tracking=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)], 'cancel': [('readonly', True)]}
    )
    date_begin = fields.Datetime(
        string='Día de inicio',
        help='Día de inicio de la carrera',
        related='career_period_id.date_begin',
        readonly=True,
        store=True,
    )
    date_end = fields.Datetime(
        string='Día de finalización',
        help='Día en que finaliza la carrera',
        related='career_period_id.date_end',
        readonly=True,
        store=True,
    )
    classroom_id = fields.Many2one(
        'classroom',
        string='Aula',
        required=True,
        tracking=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)], 'cancel': [('readonly', True)]}
    )
    subjects_ids = fields.One2many(
        'student_subject.res_partner_rel',
        'enrollment_id',
        string='Materias del estudiante',
        auto_join=True,
    )
    college_career_id = fields.Many2one(
        'college.career',
        string='Carrera',
        required=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)], 'cancel': [('readonly', True)]},
        tracking=True,
    )
