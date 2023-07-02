
from odoo import models,fields,api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    peruapis_token = fields.Text("PERUAPIS Token")


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        peruapis_token = ICPSudo.get_param("peruapis_token", default="")
        res.update(peruapis_token=peruapis_token)
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        ICPSudo.set_param("peruapis_token", self.peruapis_token or "")
