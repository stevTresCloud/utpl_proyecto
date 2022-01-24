# -*- coding: utf-8 -*-
# Copyright 2021 Trescloud <https://www.trescloud.com>

from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)


@openupgrade.logging()
def set_values(env):
    sql = '''
    SELECT id
    FROM ir_translation 
    WHERE value ilike 'Encuestas' or value ilike 'Encuesta'
    '''
    env.cr.execute(sql)
    records = env.cr.dictfetchall()
    for record in records:
        translation = env['ir.translation'].browse(record['id'])
        translation.write({'value': 'Evaluación'})


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    set_values(env)
