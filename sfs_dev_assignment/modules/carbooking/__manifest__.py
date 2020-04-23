{
    'name': 'Booking Car',
    'version': 'beta',
    'category': 'Tools for manage booking carbooking',
    'description': """

    """,
    'author': 'Simply & Fine Solutions',
    'website': 'http://www.sfsolutions.co.th/',
    'depends': ['base', 'sale_management', 'hr', 'account'],

    'data': [
        'security/ir.model.access.csv',
        # 'views/booking_car_tree_views.xml',
        'views/booking_car_views.xml',
        'views/booking_views.xml',
        'views/car_code_views.xml',
        'views/car_type_views.xml',
        'views/cars_views.xml',
        'report/booking_car_card.xml',
        'report/report.xml',
        'report/edit_sale_template.xml'
    ],

    'demo': [
    ],

    'installable': True,
    'auto_install': True,
    'application': True,
}