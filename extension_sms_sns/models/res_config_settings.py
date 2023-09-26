
from odoo import models,fields,api
import logging  

_logger = logging.getLogger("------ log de alex:")

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    id_aws = fields.Text("ID AWS")
    key_aws = fields.Text("KEY AWS")
    region_aws = fields.Text("REGION AWS")
    arn_aws = fields.Text("ARN AWS")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        ICPSudo.set_param("ID_AWS", self.id_aws or "")
        ICPSudo.set_param("key_aws", self.key_aws or "")
        ICPSudo.set_param("REGION", self.region_aws or "")
        ICPSudo.set_param("ARN", self.arn_aws or "")
    
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        id_aws = ICPSudo.get_param("ID_AWS", default="")
        key_aws = ICPSudo.get_param("key_aws", default="")
        region_aws = ICPSudo.get_param("REGION", default="")
        arn_aws = ICPSudo.get_param("ARN", default="")
        res.update(
            id_aws=id_aws,
            key_aws=key_aws,
            region_aws=region_aws,
            arn_aws=arn_aws
            )
        return res