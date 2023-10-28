from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        if self.l10n_latam_document_type_id.id == self.env.ref("l10n_pe.document_type01").id and \
            self.partner_id.l10n_latam_identification_type_id.id != self.env.ref("l10n_pe.it_RUC").id:
            raise ValidationError("Solo se puede publicar facturas para empresas con RUC o empresas no domiciliadas")
    

        super(AccountMove,self).action_post()
