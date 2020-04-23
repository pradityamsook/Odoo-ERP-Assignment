# -*- coding: utf-8 -*-
{
    'name': "MA Service",
    'summary': """MA Service""",
    'description': """MA Service """,
    'author': "Saritha",
    'category': 'Uncategorized',
    'version': '12.0.1',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/report_template.xml',
        'views/ma_report_view.xml',
        'wizards/ma_wizard.xml',
    ],
}