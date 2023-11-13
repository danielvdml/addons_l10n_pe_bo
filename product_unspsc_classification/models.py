from odoo import models,fields,api


class ProductUNSPSC(models.Model):
    _name = "product.unspsc.code"
    _description = "Códigos de producto UNSPSC"
    _rec_names_search = ['name', 'code']

    name = fields.Char(string="Nombre", required=True, translate=True)
    code = fields.Char(string="Código", required=True)
    active = fields.Boolean(string="Activo", default=True)

    @api.depends('code')
    def _compute_display_name(self):
        for prod in self:
            prod.display_name = f"{prod.code} {prod.name or ''}"

class ProductTemplate(models.Model):
    _inherit = "product.template"

    unspsc_code_id = fields.Many2one("product.unspsc.code","Clasificación de producto según UNSPSC")

