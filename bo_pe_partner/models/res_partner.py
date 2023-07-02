# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_name = fields.Char(string='Nombre comercial')
    sunat_status = fields.Char(string="SUNAT - Estado")
    sunat_condition = fields.Char(string="SUNAT - Condición")
    ubigeo = fields.Char(string='Ubigeo')

    

    @api.onchange('l10n_latam_identification_type_id', 'vat')
    def search_partner_by_vat(self):
        ICPSudo = self.env["ir.config_parameter"].sudo()
        provider = ICPSudo.get_param("provider_search_partner_by_vat", default="")
        func_search_partner_by_vat = getattr(self,"func_search_partner_by_vat_%s" % provider,None)
        if func_search_partner_by_vat:
            result = func_search_partner_by_vat()

            func_process_values_partner = getattr(self,"func_process_values_partner_%s" % provider,None)
            if func_process_values_partner:
                result = func_process_values_partner(result)
                self.update(result)
            else: 
                raise UserError("La función que procesa los datos de contactos obtenidos con el proveedor {provider} no se ha implementado. asegúrese de que la función'func_values_partner_{provider}' sea implementada.".format(provider=provider))
            