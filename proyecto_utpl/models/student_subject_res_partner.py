# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools import float_is_zero, float_round, float_compare


class StudentSubjectResPartner(models.Model):
    _name = 'student_subject.res_partner_rel'
    _table = 'student_subject_res_partner_rel'
    _description = 'Tabla de relación entre materias y Estudiantes'
    _rec_name = 'student_id'

    def _get_next_sequence(self):
        return self.env['ir.sequence'].next_by_code('res.partner.student.sequence')

    @api.depends('subject_scores_ids')
    def _compute_scores(self):
        for subject in self:
            min_score, max_score, scores_count, average = 0.0, 0.0, 0, 0.0
            approved = False
            if subject.subject_scores_ids:
                min_score = subject.subject_scores_ids.sorted('score')[0].score or 0.0
                max_score = subject.subject_scores_ids.sorted('score', reverse=True)[0].score or 0.0
                scores_count = len(subject.subject_scores_ids)
                if not float_is_zero(scores_count, precision_digits=2):
                    average = float_round(sum(subject.subject_scores_ids.mapped('score')) / scores_count, precision_digits=2)
                    if float_compare(average, subject.subject_scores_ids.mapped('student_subject_id').mapped('subject_id')[0].minimum_score_to_pass, precision_digits=2) >= 0:
                        approved = 'approved'
                    else:
                        approved = 'disapproved'
            subject.min_score = min_score
            subject.max_score = max_score
            subject.scores_count = scores_count
            subject.average = average
            subject.approved = approved

    @api.model
    def create(self, vals):
        if self._context.get('enrollment_id', False):
            vals['enrollment_id'] = self._context.get('enrollment_id')
        return super(StudentSubjectResPartner, self).create(vals)

    def button_open_scores(self):
        '''Acción para abrir asistente de eliminación de notas'''
        view_id = self.env.ref('proyecto_utpl.wizard_student_subject_view_scores_view_form').id
        action = {
            'name': 'Editar Notas',
            'view_mode': 'form',
            'res_model': 'student_subject.res_partner_rel',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'views': [[view_id, 'form']],
            'target': 'new'
        }
        return action

    name = fields.Char(
        'Materia',
        related='subject_id.name',
        store=True
    )
    subject_id = fields.Many2one(
        'student.subject',
        string='Materia',
        ondelete='cascade',
        required=True
    )
    min_score = fields.Float(
        'Nota más baja',
        help='Nota más baja del estudiante',
        compute='_compute_scores',
        store=True,
    )
    max_score = fields.Float(
        'Nota más alta',
        help='Nota más baja del estudiante',
        compute='_compute_scores',
        store=True
    )
    average = fields.Float(
        'Promedio',
        help='Promedio de la materia',
        compute='_compute_scores',
        store=True,
    )
    approved = fields.Selection(
        [('approved', 'Aprobado'),
         ('disapproved', 'Reprobado')],
        string='Estado de aprobación',
        compute='_compute_scores',
        store=True,
    )
    student_id = fields.Many2one(
        'res.partner',
        string='Estudiante',
        ondelete='cascade',
        required=True
    )
    sequence = fields.Integer(
        string='Secuencia',
        default=_get_next_sequence,
    )
    enrollment_id = fields.Many2one(
        'enrollment',
        string='Matrícula',
        ondelete='restrict',
        required=True
    )
    display_name = fields.Char(
        related='student_id.display_name',
        store=False,
        readonly=True,
    )
    subject_scores_ids = fields.One2many(
        'student.subject.scores',
        'student_subject_id',
        string='Notas de la materia',
    )
    scores_count = fields.Integer(
        string="Número de pruebas realizadas",
        compute="_compute_scores"
    )


class StudentSubjectScores(models.Model):
    _name = 'student.subject.scores'
    _description = 'Notas del estudiante, a partir de la evaluación que se contesta'

    response_id = fields.Many2one(
        'survey.user_input',
        "Prueba",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string=u'Name Score',
        help=u'Name of the score.',
        related='response_id.display_name',
        store=True,
    )
    survey_id = fields.Many2one(
        'survey.survey',
        related='response_id.survey_id',
        string="Plantilla de prueba",
        readonly=True,
        store=True
    )
    score = fields.Float(
        string='Nota',
        help='Nota',
        related='response_id.scoring_total',
        store=True,
    )
    score_percentage = fields.Float(
        string='Porcentaje de la nota',
        help='Porcentaje de la nota',
        related='response_id.scoring_total',
        store=True,
    )
    student_subject_id = fields.Many2one(
        'student_subject.res_partner_rel',
        string='Materia',
        help='Referencia de la materia',
    )
