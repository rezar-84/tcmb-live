{
    'name': 'TCMB Forex Buying Currency Provider',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Fetch Forex Buying rates from Turkish Central Bank (TCMB)',
    'author': 'ChatGPT',
    'depends': ['account_accountant'],
    'data': [
        'data/tcmb_provider_data.xml',
        'views/currency_provider_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
