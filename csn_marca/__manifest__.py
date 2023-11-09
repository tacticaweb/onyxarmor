{
    'name': 'CSN Marca',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Descripción de tu módulo personalizado',
    'description': """
        Descripción detallada de tu módulo personalizado.
    """,
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'depends': ['base', 'mrp', 'onyx_mo_marca'],  # Agrega la dependencia hacia el módulo onyx_mo_marca
    'data': [
        'views/views.xml',  # Asegúrate de incluir aquí el XML que hereda la vista de mrp.marca
    ],
    'installable': True,
    'application': False,
}
