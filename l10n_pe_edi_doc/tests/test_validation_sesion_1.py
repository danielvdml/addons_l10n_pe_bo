from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.addons.l10n_pe_edi_doc.utils.operations import suma,division,multiplicacion

@tagged('post_install','-at_install')
class TestValidationInvoiceSesion1(TransactionCase):

    def setUp(self):
        self.param1 = 3
        self.param2 = 6
        self.params = [{'a':1,'b':4,'result':5},
                        {'a':2,'b':4,'result':6},
                        {'a':3,'b':4,'result':7},
                        {'a':7,'b':2,'result':9}]
        super(TestValidationInvoiceSesion1,self).setUp()

    def test_validation_0(self):
        for item in self.params:
            result = suma(item['a'],item['b'])
            self.assertEqual(result,item['result'])


    def test_validation_1(self):
        result = suma(3,4)
        self.assertEqual(result,7)

    def test_validation_2(self):
        result = division(10,2)
        self.assertEqual(result,5)

    def test_validation_3(self):
        with self.assertRaises(ZeroDivisionError):
            result = division(10,0)
            self.assertEqual(result,0)

    def test_validation_multiplicacion_1(self):
        result = multiplicacion(8,3)
        self.assertEqual(result,24)

    def test_validation_valor_diferente_a_numero(self):
        with self.assertRaises(ValueError):
            result = multiplicacion('a',3)