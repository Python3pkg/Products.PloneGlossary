# -*- coding: utf-8 -*-
"""
$Id$
"""
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
from AccessControl import ClassSecurityInfo

# CMF imports
from Products.CMFCore  import CMFCorePermissions
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
    """PloneGlossary """
    
    portal_type = meta_type = 'PloneGlossaryDefinition'
    archetype_name = 'Glossary definition'
    immediate_view = 'ploneglossarydefinition_view'
    default_view   = 'ploneglossarydefinition_view'
    global_allow = False
    schema =  schema
    content_icon = 'ploneglossarydefinition_icon.gif'
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
