"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# ZCTextIndex patch setup

# don't patch by default
PATCH_ZCTextIndex = False

# condition for adding glossaries items in indexed text
INDEX_SEARCH_GLOSSARY = ('SearchableText',)
PORTAL_TYPES_TO_SKIP = ('PloneGlossaryDefinition',)

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
