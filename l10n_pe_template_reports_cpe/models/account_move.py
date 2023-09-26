from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.image import image_data_uri

import base64
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def generate_text_qr(self, invoice):
        ruc_emisor = invoice.company_id.partner_id.vat
        tipo_comprobante = invoice.l10n_latam_document_type_id.code
        serie = invoice.journal_id.code
        numero = invoice.name
        monto_total_igv = invoice.amount_tax
        monto_total = invoice.amount_total
        fecha = invoice.invoice_date
        tipo_documento_adquirente = invoice.partner_id.l10n_latam_identification_type_id.name if invoice.partner_id.l10n_latam_identification_type_id.name else "-"
        numero_documento = invoice.partner_id.vat if invoice.partner_id.vat else "-"

        s = ruc_emisor+"|"+tipo_comprobante+"|"+serie+"|"+numero.split("-")[1]+"|"+str(monto_total_igv)+"|"+str(monto_total)+"|"+str(fecha)+"|"+tipo_documento_adquirente+"|"+numero_documento
        
        params = {
            "barcode_type": "QR",
            'width': 128,
            'height': 128,
            'humanreadable': 1,
            "value": s            
        }
        
        # digest_value = invoice.digest_value if invoice.digest_value else "-"
        
        barcode = self.env['ir.actions.report'].barcode(**params)
        return image_data_uri(base64.b64encode(barcode))