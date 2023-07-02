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

    def func_search_partner_by_vat_peruapis(self):
        result = {}
        ICPSudo = self.env["ir.config_parameter"].sudo()
        peruapis_token = ICPSudo.get_param("peruapis_token", default="")
        if self.l10n_latam_identification_type_id:
            l10n_pe_vat_code = self.l10n_latam_identification_type_id.l10n_pe_vat_code
            if l10n_pe_vat_code in ["6","1"]:
                if peruapis_token:
                    client = PeruApis(peruapis_token)
                    if l10n_pe_vat_code == "6" and patron_ruc.match(self.vat or ""):
                        result = client.get_ruc(self.vat)
                    elif l10n_pe_vat_code == "1" and patron_dni.match(self.vat or ""):
                        result = client.get_dni(self.vat)
                else:
                    raise UserError("El Access Token de PERUAPIS no se encuentra establecido.")
        return result

    def match_peruapis(self):
        return {
            "name":"name",
            "address":"street",
            "location":"ubigeo",
            "commercial_name":"commercial_name",
            "status":"sunat_status",
            "condition":"sunat_condition"
        }

    def func_process_values_partner_peruapis(self,vals):
        match = self.match_peruapis()
        result = {}
        for key in vals:
            if vals.get(key,False) and match.get(key,False):
                result[match[key]] = vals[key]
        
        ubigeo = result.get("ubigeo",False)
        if ubigeo:
            district_id = self.env["l10n_pe.res.city.district"].search([("code","=",ubigeo)])
            city_id = district_id.city_id
            state_id = city_id.state_id
            country_id = city_id.country_id
            result.update({
                "l10n_pe_district":district_id.id,
                "city_id":city_id.id,
                "state_id":state_id.id,
                "country_id":country_id.id
            })
        return result