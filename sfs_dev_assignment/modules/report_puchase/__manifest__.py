{
    'name': 'รายงานการจัดซื้อ',
    'version': 'beta',
    'category': 'Tools for report sales',
    'description': """

    """,
    'author': 'Simply & Fine Solutions',
    'website': 'http://www.sfsolutions.co.th/',
    'depends': ['base', 'sale_management', 'hr', 'account', 'sale', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/wizard_report_purchase.xml',
        'reports/wizard_report_purchase.xml',

    ],

    'demo': [
    ],

    'installable': True,
    'auto_install': True,
    'application': True,
}