<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:regexp="http://exslt.org/regular-expressions"
  xmlns:dyn="http://exslt.org/dynamic"
  xmlns:gemfunc="http://www.sunat.gob.pe/gem/functions"
  xmlns:date="http://exslt.org/dates-and-times"
  xmlns:func="http://exslt.org/functions"
  xmlns:dp="http://www.datapower.com/extensions" extension-element-prefixes="dp" exclude-result-prefixes="dp dyn regexp date func" version="1.0">
  <!-- xsl:include href="../../../commons/error/error_utils.xsl" dp:ignore-multiple="yes" /-->
  <!-- xsl:include href="local:///commons/error/error_utils.xsl" dp:ignore-multiple="yes"/ -->
  <!-- xsl:include href="local:///commons/StringTemplates.xsl" dp:ignore-multiple="yes"/ -->

  <xsl:template name="rejectCall">
    <xsl:param name="errorCode" />
    <xsl:param name="errorMessage" />
    <xsl:param name="priority" select="'error'"/>


    <xsl:message terminate="yes">
      <xsl:value-of select="concat(' error: ', $errorMessage)" />
    </xsl:message>

  </xsl:template>

  <xsl:template name="isTrueExpresion">
    <xsl:param name="errorCodeValidate"/>
    <xsl:param name="node"/>
    <xsl:param name="expresion"/>
    <xsl:param name="isError" select="true()"/>
    <xsl:param name="descripcion" select="'INFO '"/>
    <xsl:if test="$expresion = true()">
      <xsl:choose>
        <xsl:when test="$isError">
          <xsl:call-template name="rejectCall">
            <xsl:with-param name="errorCode" select="$errorCodeValidate"/>
            <xsl:with-param name="errorMessage" select="concat($descripcion,': errorCode ', $errorCodeValidate,' (nodo: &quot;',name($node/parent::*),'/', name($node), '&quot; valor: &quot;', $node, '&quot;)')"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="addWarning">
            <xsl:with-param name="warningCode" select="$errorCodeValidate"/>
            <xsl:with-param name="warningMessage" select="concat($descripcion,': errorCode ', $errorCodeValidate,' (nodo: &quot;',name($node/parent::*),'/', name($node), '&quot; valor: &quot;', $node, '&quot;)')"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
