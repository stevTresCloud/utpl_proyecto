# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class TeacherSubjectResPartner(models.Model):
    _name = 'teacher_subject.res_partner_rel'
    _table = 'teacher_subject_res_partner_rel'
    _description = 'Tabla de relación entre materias y Profesores'
    _rec_name = 'teacher_id'

    def _get_next_sequence(self):
        return self.env['ir.sequence'].next_by_code('res.partner.teacher.sequence')

    name = fields.Char()
    subject_id = fields.Many2one(
        'student.subject',
        string='Materia',
        ondelete='cascade',
        required=True
    )
    teacher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Profesor',
        ondelete='cascade',
        required=True
    )
    sequence = fields.Integer(
        string='Secuencia',
        default=_get_next_sequence,
    )
    display_name = fields.Char(
        related='teacher_id.display_name',
        store=False,
        readonly=True,
    )
