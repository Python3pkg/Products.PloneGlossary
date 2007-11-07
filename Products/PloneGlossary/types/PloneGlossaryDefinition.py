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

# Python imports
from AccessControl import ClassSecurityInfo

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
    
from Products.CMFCore.utils import getToolByName

# Archetypes imports
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

# Products imports
from Products.PloneGlossary.config import PROJECTNAME, PLONEGLOSSARY_CATALOG
from Products.PloneGlossary.types.schemata import PloneGlossaryDefinitionSchema as schema
from Products.PloneGlossary.utils import html2text, text2words

class PloneGlossaryDefinition(BaseContent):
    """PloneGlossary definition """
    
    portal_type = meta_type = 'PloneGlossaryDefinition'
    archetype_name = 'Glossary definition'
    immediate_view = 'ploneglossarydefinition_view'
    default_view   = 'ploneglossarydefinition_view'
    global_allow = False
    schema =  schema
    content_icon = 'ploneglossarydefinition_icon.gif'
    _at_rename_after_creation = True
    
    security = ClassSecurityInfo()

    actions = (
        {
        'id'            : 'view',
        'name'          : 'View',
        'action'        : 'string:${object_url}/ploneglossarydefinition_view',
        'permissions'   : (CMFCorePermissions.View, ),
        'category'      : 'object',
        'visible'       : 1,
        },
        {
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (CMFCorePermissions.ManageProperties,),
        'category'      : 'object',
         },
        )

    security.declareProtected(CMFCorePermissions.View, 'Description')
    def Description(self, from_catalog=False):
        """Returns cleaned text"""
        
        if from_catalog:
            cat = self.getCatalog()
            brains = cat.searchResults(id=self.getId())
            
            if not brains:
                return self.Description()
            
            brain = brains[0]
            return brain.Description
        else:
            html = self.getDefinition()
            return html2text(html)
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'indexObject')
    def indexObject(self):
        """Index object in portal catalog and glossary catalog"""
        BaseContent.indexObject(self)
        cat = self.getCatalog()
        cat.indexObject(self)
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'unindexObject')
    def unindexObject(self):
        """Unindex object in portal catalog and glossary catalog"""
        BaseContent.unindexObject(self)
        cat = self.getCatalog()
        cat.unindexObject(self)
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        """Reindex object in portal catalog and glossary catalog"""
        BaseContent.reindexObject(self, idxs)
        cat = self.getCatalog()
        cat.reindexObject(self, idxs)

registerType(PloneGlossaryDefinition, PROJECTNAME)
