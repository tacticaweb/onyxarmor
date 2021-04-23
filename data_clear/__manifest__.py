# -*- coding: utf-8 -*-
{
    'author': 'Dmmsys 124358678@qq.com ',
    'name': 'Data Clear Tools',
    'category': 'Extra Tools',
    'sequence': 1,
    'summary': """A powerful testing tool.Easily clear any odoo object data what you want. """,
    'website': 'www.bonainfo.com',
    'version': '3.0',   
    'description': """Business Testing Data Clear. You can define default model group list by yourself to help your work. """,
    'license': 'LGPL-3',
    'support': '124358678@qq.com, bower_guo@msn.com',
    'price': '18',
    'currency:': 'EUR',
    'images': ['static/description/main_banner.png'],

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/clear_data.xml',
        'security/ir.model.access.csv',
        'views/clear_data_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
