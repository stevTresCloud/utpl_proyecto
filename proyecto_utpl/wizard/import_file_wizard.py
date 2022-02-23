# -*- coding: utf-8 -*-

import base64

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import os
import logging
import pathlib

_logger = logging.getLogger(__name__)


class ImportFileWizard(models.TransientModel):
    _name = 'import.file.wizard'
    _description = 'Wizard para importación de archivos a evaluación.'

    @api.model
    def default_get(self, fields):
        '''
        Se obtiene los datos del archivo adjunto, si es que se tuviere para sobreescribir. Además se manda la referencia de la evaluación en el wizard.
        '''
        res = super(ImportFileWizard, self).default_get(fields)
        active_survey_id = self.env.context.get('active_id', False)
        ir_attachment = self.env['ir.attachment'].search(
            [('res_id', '=', active_survey_id),
             ('res_model', '=', 'survey.survey')]
        )
        survey_id = self.env['survey.survey'].browse(active_survey_id)
        if res and ir_attachment:
            res['filename'] = ir_attachment.name
            res['old_attachment_id'] = ir_attachment
            res['datas'] = base64.b64decode(ir_attachment.datas)
            res['description'] = ir_attachment.description
            res['mimetype'] = ir_attachment.mimetype
            res['reference_image'] = survey_id.reference_image if survey_id.reference_image else False
        res['survey_id'] = active_survey_id
        res['has_file'] = True if survey_id and survey_id.attachment_id else False
        return res

    def action_import_file(self):
        '''
        Se importa el archivo y se realizan algunas validaciones
        '''
        self.ensure_one()
        alternative_path = os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1]
        path = '/'.join(alternative_path) + '/static/gltf/'
        active_survey_id = self.env.context.get('active_id', False)
        if not active_survey_id:
            raise ValidationError(
                u'No se ha encontrado el id del modelo survey.survey '
            )
        survey_id = self.env['survey.survey'].browse(active_survey_id)
        attachment_name = self.filename
        url_file = os.path.join(path, attachment_name)
        database_file = []
        for i, path in enumerate(list(reversed(os.path.dirname(os.path.realpath(__file__)).split('/')[0:-1]))):
            if i < 1:
                database_file.append(path)
            else:
                break
        db_url = '/'.join(database_file) + '/static/gltf/'
        db_url = os.path.join(db_url, attachment_name)
        if self.is_rewrite_file or not self.has_file:
            data_file = base64.b64decode(self.data)
            if self.has_file:
                os.remove(url_file)
            with open(url_file, 'wb') as f:
                f.write(data_file)
        if not self.has_file:
            survey_id.write({
                'attachment_id': self.env['ir.attachment'].create(
                    self._create_import_file_attachment_data(
                        active_survey_id,
                        attachment_name,
                        db_url,
                        description=self.description if self.description else None,
                        mimetype=self.mimetype if self.mimetype else None)
                ).id,
            })
        if self.has_file and self.is_rewrite_file:
            survey_id.attachment_id.write({
                'name': attachment_name,
                'url': db_url,
                'mimetype': self.mimetype,
                'description': self.description or False,
            })
        survey_id.write({
            'file_name': attachment_name,
            'reference_image': self.reference_image,
            'db_filename': self.db_filename,
        })
        return True

    @api.model
    def _create_import_file_attachment_data(self, survey_survey_id, filename, url, description=None,
                                            mimetype=None):
        '''
        Datos necesarios para creación de archivo
        '''
        return {
            'name': filename or '<unknown>',
            'res_model': 'survey.survey',
            'res_id': survey_survey_id,
            'type': 'url',
            'public': True,
            'mimetype': mimetype or 'model/gltf+json',
            'url': url,
            'description': description or False,
        }

    @api.onchange('db_filename', 'data')
    def onchange_db_filename(self):
        if self.data and not self.filename:
            file_extention = pathlib.Path(self.db_filename).suffix
            file_sequence = self.env['ir.sequence'].next_by_code('survey.survey')
            self.filename = file_sequence + file_extention

    reference_image = fields.Image("Imagen de referencia", help='Imagen de referencia para el objeto GLTF, que se mostrará en e formulario del backend')
    data = fields.Binary('Archivo', attachment=True, help='Archivo a cargar en el sistema')
    filename = fields.Char('Nombre del archivo', required=True, readonly=True, help='Nombre del archivo')
    db_filename = fields.Char('Nombre del archivo BD', required=True, readonly=True, help='Nombre del archivo a guardar en la BD')
    description = fields.Text(string='Descripción del archivo', help='Descripción del archivo')
    mimetype = fields.Char(string='Tipo de dato', required=True, default='model/gltf+json', help='Tipo de dato de archivo a cargar en el sistema.')
    is_rewrite_file = fields.Boolean('¿Desea sobreescribir?', default=True, help='Si se desea sobreescribir el archivo o no')
    has_file = fields.Boolean('Ya tiene un archivo', readonly=True, help='Evalúa si se tiene una rchivo adjunto o no')
    old_attachment_id = fields.Many2one('ir.attachment', 'Archivo antiguo importado', readonly=True, help='Archivo antiguo ya cargado en el sistema.')
    datas_old_file = fields.Binary('Archivo', required=True, attachment=True, help='Datos del archivo antiguo')
    survey_id = fields.Many2one('survey.survey', string="Evaluación", readonly=True, help='Evaluación referenciada a la que se le añadirá el archivo GLTF')
