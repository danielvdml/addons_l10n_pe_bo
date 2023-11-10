from odoo.tests.common import TransactionCase,SingleTransactionCase
from odoo.tests import tagged
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


@tagged('post_install','-at_install')
class TestValidationAccountMovePeru(SingleTransactionCase):

    def setUp(self):
        self.common()
        super(TestValidationAccountMovePeru,self).setUp()

    

    def common(self):
        partner = self.env["res.partner"]
        
        journal = self.env["account.journal"]

        #Diferentes tipos de empresas
        self.empresa = partner.create({
            "name":"ALICORP SAA",
            "l10n_latam_identification_type_id":self.env.ref("l10n_pe.it_RUC").id,
            "vat":"20100055237"
        })

        self.cliente_sin_empresa = partner.create({
            "name":"DANIEL MORENO",
            "l10n_latam_identification_type_id":self.env.ref("l10n_pe.it_DNI").id,
            "vat":"76310420"
        })

        #Diario
        self.diario = journal.create({
            "name":"Factura",
            "code":"FAC",
            "company_id":self.env.ref("base.main_company").id,
            "invoice_reference_type":"invoice",
            "type":"sale",
            "invoice_reference_model":"odoo"
        })

        #Productos
        self.product_sin_impuestos = self.env['product.product'].create({
            'name': 'product_pe',
            'weight': 2,
            'uom_po_id': self.env.ref('uom.product_uom_kgm').id,
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
            'lst_price': 1000.0,
        })

        self.product_con_impuestos = self.env['product.product'].create({
            'name': 'product_pe',
            'weight': 2,
            'uom_po_id': self.env.ref('uom.product_uom_kgm').id,
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
            'lst_price': 1000.0,
        })

    #Restricción, Cuando la factura se publica, valida que el tipo y número de identidad del cliente sea correcto
    
    def factura_1(self):        
        move = self.env["account.move"]
        self.factura = move.create({
            "partner_id":self.empresa.id,
            "currency_id":self.env.ref("base.PEN").id,
            "date":datetime.today(),
            "move_type":"out_invoice",
            "journal_id":self.diario.id,
            "l10n_latam_document_type_id":self.env.ref("l10n_pe.document_type01").id
        })
        self.factura.invoice_line_ids = [(0,0,{
            'product_id': self.product_sin_impuestos.id,
            'product_uom_id': self.env.ref('uom.product_uom_kgm').id,
            'price_unit': 2000.0,
            'quantity': 5,
            'discount': 20.0
        })]
        #_logger.info(self.factura.read())
        self.factura.action_post()
        self.assertEqual(self.factura.state, "posted")

    def factura_2(self):

        move = self.env["account.move"]
        self.factura_2 = move.create({
            "partner_id":self.cliente_sin_empresa.id,
            "currency_id":self.env.ref("base.PEN").id,
            "date":datetime.today(),
            "move_type":"out_invoice",
            "journal_id":self.diario.id,
            "l10n_latam_document_type_id":self.env.ref("l10n_pe.document_type01").id
        })
        self.factura_2.invoice_line_ids = [(0,0,{
            'product_id': self.product_sin_impuestos.id,
            'product_uom_id': self.env.ref('uom.product_uom_kgm').id,
            'price_unit': 2000.0,
            'quantity': 5,
            'discount': 20.0
        })]
        #_logger.info(self.factura.read())
        with self.assertRaises(ValidationError):
            self.factura_2.action_post()

    