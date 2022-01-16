# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class StudentSubject(models.Model):
    _name = 'student.subject'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Materias del estudiante'

    def _default_minimum_score_to_pass(self):
        return self.env.company.property_default_minimum_score_to_pass

    @api.model
    def create(self, vals):
        return super(StudentSubject, self).create(vals)

    name = fields.Char(
        string='Nombre',
        help='Nombre de la materia',
        required=True,
        )
    active = fields.Boolean('Estado', default=True)
    minimum_score_to_pass = fields.Float(
        'Puntaje mínimo para aprobar',
        help='Puntaje mínimo para aprobar',
        required=True,
        default=_default_minimum_score_to_pass,
    )
    sequence = fields.Integer('Secuencia', default=10)
    student_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='student_subject_res_partner_rel',
        column1='subject_id',
        column2='student_id',
        string='Estudiantes',
        domain=[('type_partner', '=', 'student')],
        help='Relación materia - estudiante',
        )
    teacher_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='teacher_subject_res_partner_rel',
        column1='subject_id',
        column2='teacher_id',
        domain=[('type_partner', '=', 'teacher')],
        string='Profesores',
        help='Profesores que imparten la materia',
    )
