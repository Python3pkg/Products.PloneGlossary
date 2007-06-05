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

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions

PROJECTNAME = 'PloneGlossary'
GLOBALS = globals()
SKINS_DIR = 'skins'
CONFIGLET_ICON = "ploneglossary_tool.gif"
PLONEGLOSSARY_TOOL = 'portal_glossary'
PLONEGLOSSARY_CATALOG = 'glossary_catalog'
PLONEGLOSSARY_CHARSET = 'UTF-8'
DEBUG = False
INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE = 'PLONEGLOSSARY_INSTALL_EXAMPLES'

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
