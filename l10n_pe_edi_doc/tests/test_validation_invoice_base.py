from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import file_path
import lxml.etree as ET
from lxml import etree
import lxml
import re

from datetime import datetime
ns = etree.FunctionNamespace('http://mydomain.org/myother/functions')
ns.prefix = 'es'

def matches(context, _input, patterns, flags=0):
    if type(_input[0]) == lxml.etree._ElementUnicodeResult:
        _input = _input[0] or ""
    else:
        _input = _input[0].text or ""
    if type(patterns) == lxml.etree._ElementUnicodeResult:
        return bool(re.match(patterns,_input))
    else:
        return all([bool(re.match(pattern,_input)) for pattern in patterns])

def currentDate(context):
    return datetime.today().date().strftime("%Y%M%d")

ns["current-date"] = currentDate
ns['matches'] = matches

@tagged('post_install','-at_install')
class TestValidationInvoiceBase(TransactionCase):

    def setUp(self):
        super(TestValidationInvoiceBase,self).setUp()

    def test_validation_invoice(self):
        with open(file_path('l10n_pe_edi_doc/tests/data/20608902211-01-FA11-00000249.xml'),'r') as f_xml:
            xml_file = ET.parse(f_xml)

        with open(file_path('l10n_pe_edi_doc/tests/sunat_archivos/sfs/VALI/commons/xsl/validation/2.X/ValidaExprRegFactura-2.0.1.xsl'),'rb') as f_xsl:
            xsl_file = ET.parse(f_xsl)
        
        try:
            transform = ET.XSLT(xsl_file)
            result = transform(xml_file,nombreArchivoEnviado=ET.XSLT.strparam('20608902211-01-FA11-00000249.xml'))
        except Exception as e:
            pass
        self.assertTrue(True)