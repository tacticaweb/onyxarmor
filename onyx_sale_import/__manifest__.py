# -*- coding: utf-8 -*-
{
    'name': "muebles_import",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Luis Miguel Varón E - Soluciones Open Source",
    'website': "http://www.solucionesos.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','onyx_sizing_v2_custom'],

    # always loaded
    'data': [
        'views/views.xml',
        'data/products.xml',
    ],
    # only loaded in demonstration mode
    
}