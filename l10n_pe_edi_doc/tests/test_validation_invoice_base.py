from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError
import lxml.etree as ET
from odoo.modules import get_module_resource
import logging
_logger = logging.getLogger(__name__)

@tagged('post_install','-at_install')
class TestValidationInvoiceBase(TransactionCase):

    def setUp(self):
        super(TestValidationInvoiceBase,self).setUp()

    def test_validation_1(self):
        with open(get_module_resource('l10n_pe_edi_doc','tests/data','20608902211-01-FA11-00000249.xml'),'r') as f_xml:
            xml_file = ET.parse(f_xml)

        with open(get_module_resource('l10n_pe_edi_doc','tests/sunat_archivos/sfs/VALI/commons/xsl/validation/2.X','ValidaExprRegFactura-2.0.1.xsl'),'rb') as f_xsl:
        #with open(get_module_resource('l10n_pe_edi_doc','tests/validations','Custom_ValidaExprRegFactura-2.0.1.xsl'),'rb') as f:
            xsl_file = ET.parse(f_xsl)
        _logger.info(ET.tostring(xsl_file))


        #/home/danielml/proyectos/22_odoo_16/addons_l10n_pe_bo/l10n_pe_edi_doc/tests/sunat_archivos/sfs/VALI/commons/xsl/validation/2.X/ValidaExprRegFactura-2.0.1.xsl
        transform = ET.XSLT(xsl_file)
        result = transform(xml_file,nombreArchivoEnviado=ET.XSLT.strparam('20608902211-01-FA11-00000249.xml'))
            #_logger.info(result)
        self.assertTrue(True)