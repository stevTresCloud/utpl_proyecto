# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Classroom(models.Model):
    _name = 'classroom'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Aula del estudiante'

    def _compute_student_ids(self):
        for classrom in self:
            students_ids = self.env['enrollment'].search([('classroom_id', '=', classrom.id), ('state', '=', 'matriculate')])
            classrom.enrolled_students_count = len(students_ids)
            classrom.student_ids = students_ids.mapped('student_partner_id')

    def write(self, vals):
        res = super(Classroom, self).write(vals)
        if 'code' in vals:
            for classrom in self:
                classrom.sequence_id.sudo().prefix = classrom.code
        return res

    @api.model
    def create(self, vals):
        vals_sequence = {
            'name': 'Secuencia de aula %s' % vals['name'],
            'code': 'classroom.%s' % vals['code'],
            'implementation': 'no_gap',
            'prefix': vals['code'],
            'suffix': '',
            'padding': 3,
            'company_id': vals['company_id']}
        sequence = self.env['ir.sequence'].create(vals_sequence)
        vals['sequence_id'] = sequence.id
        return super(Classroom, self).create(vals)

    def name_get(self):
        """
        Este metodo hace que se muestre el atributo 'name' (código)
        en los campos de relación con este modelo.
        :return:
        """
        res = super(Classroom, self).name_get()
        if self._context.get('show_students_count', False):
            return list(map(lambda record: tuple([record.id, "%s %s/%s" % (record.name, record.enrolled_students_count, record.number_limit_students)]), self))
        return res

    name = fields.Char(
        'Nombre del Aula',
        required=True,
    )
    code = fields.Char(
        'Código de Aula',
        required=True,
        related='sequence_id.prefix',
        help='Código de aula con el que se creará la matrícula de los estudiantes.'
    )
    enrolled_students_count = fields.Integer(
        'Estudiantes matriculados',
        compute='_compute_student_ids',
        help='Número de estudiantes matriculados en esta aula.',
    )
    sequence_id = fields.Many2one(
        'ir.sequence',
        help='Secuencia que se utilizará para la matriculación de los estudiantes',
        check_company=True,
        readonly=True,
        ondelete='restrict',
        copy=False
    )
    number_limit_students = fields.Integer(
        'Límite de estudiantes',
        required=True,
        help='Número límite de estudiantes que se podrán matricular en el aula.',
    )
    active = fields.Boolean(
        'Estado',
        default=True
    )
    sequence = fields.Integer(
        'Secuencia',
        default=10
    )
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company
    )
    student_ids = fields.One2many(
        'res.partner',
        'classrom_number',
        string='Estudiantes',
        compute='_compute_student_ids',
        store=True,
        domain=[('active', '=', True), ('type_partner', '=', 'student')]
    )
    description = fields.Char(
        string=u'Descripción',
        help=u'Descripción del periodo lectivo',
        copy=False
    )
