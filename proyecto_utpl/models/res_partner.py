# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.tools import float_is_zero, float_round, float_compare


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('student_subjects_ids', 'student_subjects_ids.subject_scores_ids')
    def _compute_student_scores(self):
        for partner in self:
            min_score, max_score, average, general_approved_status = 0.0, 0.0, 0.0, False
            if partner.type_partner == 'student' and partner.student_subjects_ids:
                if partner.student_subjects_ids:
                    min_score = partner.student_subjects_ids.sorted('min_score')[0].min_score if partner.student_subjects_ids.sorted('min_score') else False
                    max_score = partner.student_subjects_ids.sorted('max_score')[0].max_score if partner.student_subjects_ids.sorted('min_score') else False
                    if not float_is_zero(len(partner.student_subjects_ids), precision_digits=2):
                        average = float_round(sum(partner.student_subjects_ids.mapped('average')) / len(partner.student_subjects_ids), precision_digits=2)
                        if float_compare(average, self.env.company.property_default_minimum_score_to_pass, precision_digits=2) >= 0:
                            general_approved_status = 'approved'
                        else:
                            general_approved_status = 'disapproved'
                partner.min_score = min_score
                partner.max_score = max_score
                partner.average = average
                partner.general_approved_status = general_approved_status

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

    type_partner = fields.Selection(
        [('native', 'Ninguno'),
         ('teacher', 'Profesor'),
         ('student', 'Estudiante')],
        string='Tipo de contacto',
        default='native',
        required=True,
    )
    compute_user_type = fields.fields.Many2one(
        'res.groups',
        help='Tipo de usuario',
        compute='_compute_user_type',
        store=True,
        copy=False
    )
    classrom_number = fields.Many2one(
        'classroom',
        help='Número de clase en la que estará matriculado el estudiante.',
        store=True,
        copy=False
    )
    teacher_subjects_ids = fields.One2many(
        'teacher_subject.res_partner_rel',
        'teacher_id',
        string='Materias del profesor',
        auto_join=True,
    )
    student_subjects_ids = fields.One2many(
        'student_subject.res_partner_rel',
        'student_id',
        string='Materias del estudiante',
        auto_join=True,
    )
    enrollment_id = fields.Many2one(
        'enrollment',
        string='Matricula del estudiante',
        help='Matricula del estudiante',
        check_company=True,
        readonly=True,
        ondelete='restrict',
        copy=False,
    )
    min_score = fields.Float(
        string='Nota más baja',
        compute='_compute_student_scores',
        store=True,
        copy=False,
    )
    max_score = fields.Float(
        string='Nota más alta',
        compute='_compute_student_scores',
        store=True,
        copy=False,
    )
    average = fields.Float(
        'Promedio general',
        help='Promedio de la materia',
        compute='_compute_student_scores',
        store=True,
        copy=False,
    )
    general_approved_status = fields.Selection(
        [('approved', 'Aprobado'),
         ('disapproved', 'Reprobado')],
        string='Estado de aprobación general',
        compute='_compute_student_scores',
        store=True,
        copy=False,
    )
