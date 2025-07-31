{
    'name': 'Sale Auto Process Config',
    'version': '18.0.0.0.0',
    'category': 'Sales',
    'summary': 'Auto-confirm Delivery, Invoice & Payment on Sales Order Confirmation',
        'description': """
This module allows full automation of the sales order workflow:
- Automatically validate the Delivery Order
- Automatically generate and post the Invoice
- Automatically register Payment if configured
    """,
    'author': 'Syeda Khadizatul Maria, Cenote Soft',
    'company': 'Cenote Soft',
    'maintainer': 'Cenote Soft',
    'website': "https://cenotesoft.com/",
    'category': 'Sales',
    'depends': ['sale_management', 'stock', 'account'],
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.jpeg'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
