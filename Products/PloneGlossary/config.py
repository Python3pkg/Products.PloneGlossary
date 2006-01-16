"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# CMF imports
from Products.CMFCore import CMFCorePermissions

PROJECTNAME = 'PloneGlossary'
GLOBALS = globals()
SKINS_DIR = 'skins'
CONFIGLET_ICON = "ploneglossary_tool.gif"
PLONEGLOSSARY_TOOL = 'portal_glossary'
PLONEGLOSSARY_CATALOG = 'glossary_catalog'
PLONEGLOSSARY_CHARSET = 'UTF-8'


# Configlets
ploneglossary_prefs_configlet = {
    'id': 'ploneglossary_prefs',
    'appId': PROJECTNAME,
    'name': 'PloneGlossary preferences',
    'action': 'string:$portal_url/ploneglossary_management_form',
    'category': 'Products',
    'permission': (CMFCorePermissions.ManagePortal,),
    'imageUrl': CONFIGLET_ICON,
    }
