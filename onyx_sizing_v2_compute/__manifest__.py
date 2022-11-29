# -*- coding: utf-8 -*-
{
    'name': 'Onyx Armour - Sizing Compute',
    'description': "Modulo de calculo de tallaje",
    'author': "SOLUCIONES OPEN SOURCE",
    'website': "http://www.solucionesos.com",
    'summary': "Onyx - Agent Sizing Compute",
    'version': '0.1',
    "license": "OPL-1",
    'support': 'luis.varon@tacticaweb.com.co',
    'category': 'module_category_project',
        # any module necessary for this one to work correctly
    'depends': ['onyx_sizing_v2_custom'],

    # always loaded
    'data': [
        'views/views.xml',
            ],
    'qweb': [
               
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}