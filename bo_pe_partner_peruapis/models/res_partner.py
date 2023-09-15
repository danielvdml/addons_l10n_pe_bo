from odoo import models,api,fields
from odoo.addons.bo_apiservices_peruapis.service import PeruApis
from odoo.exceptions import UserError, ValidationError
import logging
import re
_logger = logging.getLogger(__name__)

patron_ruc = re.compile('[12]\d{10}$')
patron_dni = re.compile('\d{8}$')

class ResPartner(models.Model):
    _inherit = "res.partner"



    def _search_partner_by_vat_peruapis(self):
        result = {}
        ICPSudo = self.env["ir.config_parameter"].sudo()
        peruapis_token = ICPSudo.get_param("peruapis_token", default="")
        if self.l10n_latam_identification_type_id:
            l10n_pe_vat_code = self.l10n_latam_identification_type_id.l10n_pe_vat_code
            if l10n_pe_vat_code in ["6","1"]:
                if peruapis_token:
                    client = PeruApis(peruapis_token)
                    force = self.env.context.get("peruapis_force",False)
                    if l10n_pe_vat_code == "6" and patron_ruc.match(self.vat or ""):
                        result = client.get_ruc(self.vat,force)
                    elif l10n_pe_vat_code == "1" and patron_dni.match(self.vat or ""):
                        result = client.get_dni(self.vat,force)
                else:
                    raise UserError("El Access Token de PERUAPIS no se encuentra establecido.")
        _logger.info(result)
        return result

    def _match_fields_peruapis(self):
        return {
            "name":"name",
            "address":"street",
            "location":"ubigeo",
        }

    def _process_values_partner_peruapis(self,result,vals):
        if "fullname" in vals:
            result.update(name = vals.get("fullname"))

        return result