{
    'name': 'Promotions',
    'version': '1.0',
    'category': 'Extra Tools',
    'description': """

    """,
    'author': 'Simply & Fine Solutions',
    'website': 'http://www.sfsolutions.co.th/',
    'depends': ['base', 'sale', 'account', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/promotions_view.xml',
        'views/sale.xml',
    ],

    'demo': [
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}