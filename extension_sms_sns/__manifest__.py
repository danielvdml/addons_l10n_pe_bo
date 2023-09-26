{
    'name': 'SMS por AWS SNS',
    'version': '1.0',
    'summary': 'Envia mensajes de texto con aws sns',
    'description': 'Este módulo extiende la funcionalidad de envío de mensajes',
    'author': 'Alex Rodriguez',
    'category': 'Contactos',
    'depends': ['base','contacts','sms'],
    'data': [
        'views/contact.xml',
        'views/sns_sms_credentials.xml',
        'views/sms_composer_view.xml',
    ],
}
