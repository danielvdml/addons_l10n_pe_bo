from odoo import models,api,fields
from odoo.addons.bo_apiservices_apimigo.service import ApiMigo
from odoo.exceptions import UserError, ValidationError
import logging
import re
_logger = logging.getLogger(__name__)

patron_ruc = re.compile('[12]\d{10}$')
patron_dni = re.compile('\d{8}$')

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _search_partner_by_vat_apimigo(self):
        result = {}
        ICPSudo = self.env["ir.config_parameter"].sudo()
        apimigo_token = ICPSudo.get_param("apimigo_token", default="")
        if self.l10n_latam_identification_type_id:
            l10n_pe_vat_code = self.l10n_latam_identification_type_id.l10n_pe_vat_code
            if l10n_pe_vat_code in ["6","1"]:
                if apimigo_token:
                    client = ApiMigo(apimigo_token)
                    if l10n_pe_vat_code == "6" and patron_ruc.match(self.vat or ""):
                        result = client.get_ruc(self.vat)
                    elif l10n_pe_vat_code == "1" and patron_dni.match(self.vat or ""):
                        result = client.get_dni(self.vat)
                    _logger.info(result)
                else:
                    raise UserError("El Access Token de APIMIGO no se encuentra establecido.")
        return result


    def _match_fields_apimigo(self):
        return {
            "direccion":"street",
            "direccion_simple":"street2",
            "ubigeo":"ubigeo"
        }
    
    def _process_values_partner_apimigo(self,result,vals):
        if "dni" in vals:
            result.update(name = vals.get("nombre",False))
        elif "ruc" in vals:
            result.update(name = vals.get("nombre_o_razon_social","-"))
            
        return result
        