# -*- coding: utf-8 -*-
"""
$Id$
"""
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
from StringIO import StringIO
import string

# Zope imports
from Acquisition import aq_base

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal

# Archetypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes

# Product import
from Products.PloneGlossary.PloneGlossaryTool import PloneGlossaryTool
from Products.PloneGlossary.config import \
    PROJECTNAME, \
    GLOBALS, \
    PLONEGLOSSARY_TOOL, \
    ploneglossary_prefs_configlet

def install_tool(self, out):
    """Install PloneGlossary tool"""
    
    tool = getToolByName(self, PLONEGLOSSARY_TOOL, None)
    
    if tool is None:
        #Add a tool to manage vocabulary
        add_tool = self.manage_addProduct[PROJECTNAME].manage_addTool
        add_tool(PloneGlossaryTool.meta_type)
        tool = getToolByName(self, PLONEGLOSSARY_TOOL)
        print >>out, 'PloneGlossary tool installed.\n'
    else:
        # Make sure properties are updated
        tool.initProperties()

glossary_portlets = ('here/portlet_ploneglossary/macros/portlet',)

def install_portlet(self, out):
    """Install portlet in right slots"""
    
    utool = getToolByName(self, 'portal_url')
    portal = utool.getPortalObject()
    portlets = list(portal.getProperty('right_slots'))
    
    for portlet in glossary_portlets:
        if portlet not in portlets:
            portlets.append(portlet)
    
    portal._updateProperty('right_slots', portlets)
 
    print >>out, 'PloneGlossary portlet installed.\n'

def uninstall_portlet(self, out):
    """Install portlet in right slots"""
    
    utool = getToolByName(self, 'portal_url')
    portal = utool.getPortalObject()
    portlets = list(portal.getProperty('right_slots'))
    
    for portlet in glossary_portlets:
        if portlet in portlets:
            portlets.remove(portlet)
    
    portal._updateProperty('right_slots', portlets)
    
    print >>out, 'PloneGlossary portlet installed.\n'

def install(self):
    """Install PloneGlossary product"""
    out = StringIO()

    # Install types and "switch" external methods
    typeInfo = listTypes(PROJECTNAME)
    installTypes(self, out,
                 typeInfo,
                 PROJECTNAME)

    # Install tools
    install_tool(self, out)
    
    # Install skin
    install_subskin(self, out, GLOBALS)
    
    # Install portlet in right slots
    install_portlet(self, out)
    
    # Install configlet
    cp_tool = getToolByName(self, 'portal_controlpanel')
    cp_tool.registerConfiglet(**ploneglossary_prefs_configlet)
    
    out.write('Installation completed.\n')
    return out.getvalue()

def uninstall(self):
    """Uninstall PloneGlossary product"""
    out = StringIO()
    
    # Uninstall portlet in right slots
    uninstall_portlet(self, out)
    
    # Uninstall configlets
    try:
        cp_tool = getToolByName(self, 'portal_controlpanel')
        cp_tool.unregisterApplication(PROJECTNAME)
    except:
        pass
    
    out.write('Uninstallation completed.\n')
    return out.getvalue()
