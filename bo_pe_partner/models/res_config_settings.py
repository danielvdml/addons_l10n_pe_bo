
from odoo import models,fields,api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    provider_search_partner_by_vat = fields.Selection(selection=[("none","Ninguno")],string="Proveedor de consulta RUC/DNI")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        provider_search_partner_by_vat = ICPSudo.get_param("provider_search_partner_by_vat", default="")
        res.update(provider_search_partner_by_vat=provider_search_partner_by_vat)
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        ICPSudo.set_param("provider_search_partner_by_vat", self.provider_search_partner_by_vat or "")


    