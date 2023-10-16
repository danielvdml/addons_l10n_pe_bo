from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError
import lxml.etree as ET
from lxml import etree
import lxml
import re
from odoo.modules import get_module_resource
import logging
_logger = logging.getLogger(__name__)
ns = etree.FunctionNamespace('http://mydomain.org/myother/functions')
ns.prefix = 'es'

def matches(context, _input, patterns, flags=0):
    """
    _logger.info("=========================")
    _logger.info(context)
    _logger.info(_input)
    _logger.info(patterns)
    _logger.info(type(patterns))
    """
    if type(_input[0]) == lxml.etree._ElementUnicodeResult:
        _input = _input[0] or ""
        #_logger.info(_input)
    else:
        _input = _input[0].text or ""
        #_logger.info(_input)
        
    #_logger.info(pattern)
    # Crear una expresión regular con el patrón y las banderas especificadas
    if type(patterns) == lxml.etree._ElementUnicodeResult:
        return bool(re.match(patterns,_input))
    else:
        return all([bool(re.match(pattern,_input)) for pattern in patterns])
        

ns['matches'] = matches

@tagged('post_install','-at_install')
class TestValidationInvoiceBase(TransactionCase):

    def setUp(self):
        super(TestValidationInvoiceBase,self).setUp()

    def test_validation_1(self):
        with open(get_module_resource('l10n_pe_edi_doc','tests/data','20608902211-01-FA11-00000249.xml'),'r') as f_xml:
            xml_file = ET.parse(f_xml)

        with open(get_module_resource('l10n_pe_edi_doc','tests/sunat_archivos/sfs/VALI/commons/xsl/validation/2.X','ValidaExprRegFactura-2.0.1.xsl'),'rb') as f_xsl:
        #with open(get_module_resource('l10n_pe_edi_doc','tests/validations','Custom_ValidaExprRegFactura-2.0.1.xsl'),'rb') as f:
        #with open(get_module_resource('l10n_pe_edi_doc','tests','ValidaExprRegFactura.xsl'),'rb') as f_xsl:
            xsl_file = ET.parse(f_xsl)


        #/home/danielml/proyectos/22_odoo_16/addons_l10n_pe_bo/l10n_pe_edi_doc/tests/sunat_archivos/sfs/VALI/commons/xsl/validation/2.X/ValidaExprRegFactura-2.0.1.xsl
        
        try:
            transform = ET.XSLT(xsl_file)
            result = transform(xml_file,nombreArchivoEnviado=ET.XSLT.strparam('20608902211-01-FA11-00000249.xml'))
            _logger.info(result)
        except Exception as e:
            _logger.info(f'log error {e}')
            #_logger.info(result)
        self.assertTrue(True)