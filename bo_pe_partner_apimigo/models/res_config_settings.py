
from odoo import models,fields,api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    provider_search_partner_by_vat = fields.Selection(selection_add=[("apimigo","apimigo")])
