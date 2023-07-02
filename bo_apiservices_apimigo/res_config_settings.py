
from odoo import models,fields,api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    apimigo_token = fields.Text("Api Migo Token")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        apimigo_token = ICPSudo.get_param("apimigo_token", default="")
        res.update(apimigo_token=apimigo_token)
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        ICPSudo.set_param("apimigo_token", self.apimigo_token or "")
