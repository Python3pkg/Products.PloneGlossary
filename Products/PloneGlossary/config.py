## -*- coding: utf-8 -*-
## Copyright (C) 2007 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


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
