{
    'name': 'Plantillas de reportes CPE',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Bigodoo',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'templates/paperformat.xml',
        'templates/external_layout_background_cpe.xml',
        'templates/invoice_document.xml',
    ],
    'assets': {
        "web.report_assets_common":[
            "l10n_pe_template_reports_cpe/static/src/scss/report.scss"
        ],
    }
}