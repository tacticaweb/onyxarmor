{
    'name': 'Auto Generate Lot Number in Manufacturing WorkOrder',
    'version': '14.1.1.1',
    'category': 'Manufacturing',
    'summary': 'Auto Generate Lot/Serail number in Workorder of Manufacturing',
    'description': """ Auto Generate Lot/Serail number in Workorder of Manufacturing.
    """,
    'depends': ['mrp','stock'],
    "author" : "MAISOLUTIONSLLC",
    "email": 'apps@maisolutionsllc.com',
    "website":'http://maisolutionsllc.com/',
    'license': 'OPL-1',
    'price': 14,
    'currency': 'EUR',
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'qweb': [ ],
    'images': ['static/description/main_screenshot.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
