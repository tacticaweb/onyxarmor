# -*- coding: utf-8 -*-
{
    'name': 'Onyx Armour - Configurador de Producto con Variantes',
    'description': "Configurador de Producto",
    'author': "SOLUCIONES OPEN SOURCE",
    'website': "http://www.solucionesos.com",
    'summary': "Onyx - Agent Sizing",
    'version': '0.1',
    "license": "OPL-1",
    'support': 'luis.varon@tacticaweb.com.co',
    'category': 'module_category_project',
        # any module necessary for this one to work correctly
    'depends': ['sale','onyx_sizing_v2_custom'],
    # always loaded
    'data': [
            'views/product.xml',
            'wizard/sale_product_configurator_views.xml',
            
            ],
    'qweb': [
               
            ],
    #"external_dependencies": {"python" : ["pytesseract"]},
    'installable': True,
}
