<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:xs="http://www.w3.org/2001/XMLSchema" 
                xmlns:regexp="http://exslt.org/regular-expressions" 
                xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" 
                xmlns:ds="http://www.w3.org/2000/09/xmldsig#" 
                xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" 
                xmlns:sac="urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1" 
                xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" 
                xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 
                xmlns:dp="http://www.datapower.com/extensions" 
                xmlns:date="http://exslt.org/dates-and-times">

    <!--<xsl:include href="../tests/validate_utils.xsl"/>-->
    <xsl:include href="../tests/sunat_archivos/sfs/VALI/commons/error/validate_utils.xsl"/>

    <xsl:param name="nombreArchivoEnviado"/>
    <xsl:variable name="numeroRuc" select="substring($nombreArchivoEnviado, 1, 11)"/>
    <xsl:variable name="tipoComprobante" select="substring($nombreArchivoEnviado, 13, 2)"/>
    <xsl:variable name="numeroSerie" select="substring($nombreArchivoEnviado, 16, 4)"/>
    <xsl:variable name="numeroComprobante" select="substring($nombreArchivoEnviado, 21, string-length($nombreArchivoEnviado) - 24)"/>
        
    <xsl:template match="/*">

		<xsl:call-template name="isTrueExpresion">
			<xsl:with-param name="errorCodeValidate" select="'1034'"/>
			<xsl:with-param name="node" select="cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID"/>
			<xsl:with-param name="expresion" select="$numeroRuc != cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID"/>
		</xsl:call-template>
    </xsl:template>



</xsl:stylesheet>