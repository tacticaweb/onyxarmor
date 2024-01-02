# -*- coding: utf-8 -*-
{
    'name': 'Onyx Armour - Custom Go',
    'description': "Asociation SO-MO-GO",
    'author': "Tactica",
    'website': "tacticaweb.co",
    'summary': "Onyx - Custom GO",
    'version': '0.1',
    "license": "OPL-1",
    'support': 'soporte@puntosdeventa.co',
    'category': 'module_category_project',
        # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'views/views.xml',
            ],
    'qweb': [
               
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}