# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    #commercial_name = fields.Char(string='Nombre comercial')
    #sunat_status = fields.Char(string="SUNAT - Estado")
    #sunat_condition = fields.Char(string="SUNAT - Condición")
    ubigeo = fields.Char(string='Ubigeo')

    def _search_partner_by_vat(self,provider = ""):
        result = {}
        func_search_partner_by_vat = getattr(self,"_search_partner_by_vat_%s" % provider,None)
        if func_search_partner_by_vat:
            result = func_search_partner_by_vat()
        return result

    def _process_values_partner(self,provider = "", vals={}):
        match = self._match_fields(provider)
        result = {match[key]:"" for key in match}
        for key in vals:
            if match.get(key,False):
                result[match[key]] = vals.get(key,False)

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
        
        func_process_values_partner = getattr(self,"_process_values_partner_%s" % provider,None)
        if func_process_values_partner:
            result = func_process_values_partner(result,vals)
        return result

    def _match_fields(self,provider = ""):
        match = {}
        if provider or provider is not "none":
            func_match_fields_provider = getattr(self,"_match_fields_%s" % provider ,None)
            if func_match_fields_provider:
                match = func_match_fields_provider()
                if match == {}:
                    raise ValidationError("_match_fields debe ser implementada para el proveedor %s" % provider)
        return match
        
    @api.onchange('l10n_latam_identification_type_id', 'vat')
    def change_vat(self):
        for record in self:
            record.update(record.search_partner_by_vat())


    def search_partner_by_vat(self):
        self.ensure_one()
        result = {}
        ICPSudo = self.env["ir.config_parameter"].sudo()
        provider = ICPSudo.get_param("provider_search_partner_by_vat", default="")
        if provider or provider is not "none":
            result = self._search_partner_by_vat(provider)
            if result != {}:
                result = self._process_values_partner(provider,result)
        return result
    