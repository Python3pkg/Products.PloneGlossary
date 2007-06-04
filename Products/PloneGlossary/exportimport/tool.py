# -*- coding: utf-8 -*-
## Copyright (C) 2006 Ingeniweb - all rights reserved    
## No publication or distribution without authorization.
"""
"""
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import PropertyManagerHelpers
from Products.GenericSetup.utils import XMLAdapterBase

from Products.CMFCore.utils import getToolByName

from Products.PloneGlossary import LOG
from Products.PloneGlossary.config import PLONEGLOSSARY_TOOL
from Products.PloneGlossary.interfaces import IGlossaryTool


class ToolXMLAdapter(XMLAdapterBase, PropertyManagerHelpers):
    """
    XML import/export for IGlossaryTool
    """

    __used_for__ = IGlossaryTool

    _LOGGER_ID = 'PloneGlossary'

    name = 'glossary'

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractProperties())

        self._logger.info('Glossary tool exported.')
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeProperties()

        self._initProperties(node)

        self._logger.info('Glossary tool imported.')
    
def importGlossaryTool(context):
    """Import glossary tool settings from an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, PLONEGLOSSARY_TOOL)

    importObjects(tool, '', context)

def exportGlossaryTool(context):
    """Export glossary tool settings as an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, PLONEGLOSSARY_TOOL, None)
    if tool is None:
        LOG.info('Nothing to export.')
        return

    exportObjects(tool, '', context)
