# -*- coding: utf-8 -*-
{
    'name': 'Onyx Armour - Rename',
    'description': "Modulo Indexado y Agrupacion Lineas Factura",
    'author': "SOLUCIONES OPEN SOURCE",
    'website': "http://www.solucionesos.com",
    'summary': "Onyx - Agent Sizing Compute",
    'version': '0.1',
    "license": "OPL-1",
    'support': 'luis.varon@tacticaweb.com.co',
    'category': 'module_category_project',
        # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
            ],
    'qweb': [
               
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}
