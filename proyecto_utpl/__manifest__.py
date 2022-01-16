# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Modulo Alex',
    'version': '1.2',
    'category': 'Sales',
    'description': '''
        Modulo Alex
    ''',
    'author': 'Modulo Alex',
    'maintainer': 'Alex',
    'website': 'http://www.alex.com',
    'summary': 'Módulo Personalizado de Alex',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'survey',
        'website',
        'contacts',
    ],
    'data': [
        # Data
        'data/ir_sequence_data.xml',
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/student_subject_view.xml',
        'views/survey_survey_view.xml',
        'views/day_trip_view.xml',
        'views/career_period.xml',
        'views/res_partner_view.xml',
        'views/classroom_view.xml',
        'views/student_subject_res_partner.xml',
        'views/res_config_settings_view.xml',
        'views/res_users_view.xml',
        'views/enrollment.xml',
        'views/college_career_view.xml',
        'views/menus_view.xml',
        # Wizards
        'wizard/import_file_wizard_view.xml',

        # Templates
        'views/survey_templates.xml',
    ],
    'application': True,
    'installable': True,
}

