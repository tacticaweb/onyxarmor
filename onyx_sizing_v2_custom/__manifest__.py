# -*- coding: utf-8 -*-
{
    'name': 'Onyx Armour - Sizing',
    'description': "Modulo de tallaje",
    'author': "SOLUCIONES OPEN SOURCE",
    'website': "http://www.solucionesos.com",
    'summary': "Onyx - Agent Sizing",
    'version': '0.1',
    "license": "OPL-1",
    'support': 'luis.varon@tacticaweb.com.co',
    'category': 'module_category_project',
        # any module necessary for this one to work correctly
    'depends': ['sale', 'sale_stock','account'],

    # always loaded
    'data': [
             'views/views.xml',
             'views/templates.xml',
             'security/ir.model.access.csv',
             'data/variant_data.xml',
            ],
    'qweb': [
               
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}
