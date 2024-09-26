# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Gantt',
    'category': 'Hidden',
    'description': """
Odoo Web Gantt chart view.
=============================

""",
    'version': '2.0',
    'depends': ['web', 'project', 'project_risk_management_app'],
    'data' : [
        'views/web_gantt_templates.xml',
        'views/task_gantt_view.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'auto_install': True,
    'license': 'OEEL-1',
}
