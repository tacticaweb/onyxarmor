# -*- coding: utf-8 -*-
{
    'name': 'Onyx Armour - MO Sale Origin',
    'description': "Fix Invoice Status in Sales",
    'author': "SOLUCIONES OPEN SOURCE",
    'website': "http://www.solucionesos.com",
    'summary': "Onyx - Fix Invoice Status",
    'version': '0.1',
    "license": "OPL-1",
    'support': 'luis.varon@tacticaweb.com.co',
    'category': 'module_category_project',
        # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [
        'views/views.xml',
            ],
    'qweb': [
               
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}