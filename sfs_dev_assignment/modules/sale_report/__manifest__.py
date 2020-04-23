{
    'name': 'รายงานยอดขาย',
    'version': 'beta',
    'category': 'Tools for report sales',
    'description': """

    """,
    'author': 'Simply & Fine Solutions',
    'website': 'http://www.sfsolutions.co.th/',
    'depends': ['base', 'sale_management', 'hr', 'account', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_total_view.xml',
        'reports/wizard_print_sale_report_total.xml'
    ],

    'demo': [
    ],

    'installable': True,
    'auto_install': True,
    'application': True,
}