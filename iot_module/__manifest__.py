# -*- coding: utf-8 -*-
{
    'name': "iot_module",

    'summary': """
        Este es un prototipo para el manejo de datos con web controllers
        Solo pruebas""",

    'description': """
        Probaremos el manejo de datos desde una api externa
    """,

    'author': "Léyder Gallego",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
