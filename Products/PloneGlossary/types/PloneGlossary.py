# -*- coding: utf-8 -*-
"""
$Id$
"""
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# Zope imports
from Acquisition import aq_base

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils  import getToolByName

# Archetypes imports
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

# Products imports
from Products.PloneGlossary.config import PROJECTNAME, PLONEGLOSSARY_CATALOG
from Products.PloneGlossary.PloneGlossaryCatalog import PloneGlossaryCatalog, manage_addPloneGlossaryCatalog
from Products.PloneGlossary.types.schemata import PloneGlossarySchema as schema
from Products.PloneGlossary.utils import encode

class PloneGlossary(OrderedBaseFolder):
    """PloneGlossary container"""
    
    portal_type = meta_type = 'PloneGlossary'
    archetype_name = 'Glossary'
    immediate_view = 'ploneglossary_view'
    default_view   = 'ploneglossary_view'
    global_allow = True
    allowed_content_types = ('PloneGlossaryDefinition',)
    schema =  schema
    content_icon = 'ploneglossary_icon.gif'
    _at_rename_after_creation = True
    
    security = ClassSecurityInfo()

    actions = (
        {
        'id'            : 'view',
        'name'          : 'View',
        'action'        : 'string:${object_url}/ploneglossary_view',
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
    
      
    security.declareProtected(CMFCorePermissions.View, 'getGlossaryDefinitions')
    def getGlossaryDefinitions(self, terms):
        """Returns glossary definitions.
        Returns tuple of dictionnary title, text.
        Definition is based on catalog getText metadata."""

        # Get glossary catalog
        title_request = ' OR '.join(['"%s"' % x for x in terms if len(x) > 0])
        if not title_request:
            return []
        
        # Get # Get glossary related term brains
        cat = self.getCatalog()
        brains = cat(Title=title_request)
        if not brains:
            return []
        
        # Build definitions
        definitions = []
        mtool = getToolByName(self, 'portal_membership')
        for brain in brains:
            # Check view permission
            # FIXME: Maybe add allowed roles and user index in glossary catalog
            obj = brain.getObject()
            has_view_permission = mtool.checkPermission(CMFCorePermissions.View, obj) and mtool.checkPermission(CMFCorePermissions.AccessContentsInformation, obj)
            if not has_view_permission:
                continue
            
            # Make sure the title of glossary term is not empty 
            title = brain.Title
            if not title:
                continue
            
            # Build definition
            item = {
                'id' : brain.id, 
                'title' : brain.Title, 
                'variants' : brain.getVariants,
                'description' : brain.Description,
                'url' : brain.getURL()}
            definitions.append(item)
        
        return tuple(definitions)

    security.declareProtected(CMFCorePermissions.View, 'getGlossaryTerms')
    def getGlossaryTerms(self):
        """Returns glossary terms title."""

        # Get glossary term titles
        return [x['title'] for x in self.getGlossaryTermItems()]
    
    # Make it private because this method doesn't check term security
    def _getGlossaryTermItems(self):
        """Returns glossary terms in a specific structure
        
        Item:
        - path -> term path
        - id -> term id
        - title -> term title
        - description -> term description
        - url -> term url
        """
        
        # Returns all glossary term brains
        cat = self.getCatalog()
        brains = cat(REQUEST={})
        
        # Build items
        items = []
        for brain in brains:
            items.append({'path': brain.getPath(),
                          'id': brain.id,
                          'title': brain.Title,
                          'variants': brain.getVariants,
                          'description': brain.Description,
                          'url': brain.getURL(),})
        return items
    
    security.declarePublic('getGlossaryTermItems')
    def getGlossaryTermItems(self):
        """Returns the same list as _getGlossaryTermItems but check security."""
        
        # Get glossaries term items
        not_secured_term_items = self._getGlossaryTermItems()
        
        # Walk into each catalog of glossaries and get terms
        utool = getToolByName(self, 'portal_url')
        portal_object = utool.getPortalObject()
        term_items = []
        for item in not_secured_term_items:
            path = item['path']
            try:
                obj = portal_object.restrictedTraverse(path)
            except:
                continue
            term_items.append(item)
        return term_items
    
    security.declarePublic('getCatalog')
    def getCatalog(self):
        """Returns catalog of glossary"""
        
        if not hasattr(self, PLONEGLOSSARY_CATALOG):
            # Build catalog if it doesn't exist
            catalog = self._initCatalog()
        else : 
            catalog = getattr(self, PLONEGLOSSARY_CATALOG)

        return catalog
  
    def _initCatalog(self):
        """Add Glossary catalog"""
        
        if not hasattr(self, PLONEGLOSSARY_CATALOG):
            add_catalog = manage_addPloneGlossaryCatalog
            add_catalog(self)
        
        catalog = getattr(self, PLONEGLOSSARY_CATALOG)
        catalog.manage_reindexIndex()
        return catalog
    
    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        OrderedBaseFolder.manage_afterAdd(self, item, container)
        
        # Add catalog
        self._initCatalog()
    
    def _getSiteCharset(self):
        """Returns site charset"""
        
        # Get site charset
        ptool = getToolByName(self, 'portal_properties')
        return ptool.site_properties.default_charset
    
    security.declareProtected(CMFCorePermissions.ManagePortal, 'rebuildCatalog')
    def rebuildCatalog(self):
        """Delete old catalog of glossary and build a new one"""
        
        # Delete catalog if exists
        if hasattr(self, PLONEGLOSSARY_CATALOG):
            self.manage_delObjects([PLONEGLOSSARY_CATALOG])
            
        # Add a new one
        cat = self._initCatalog()
        
        # Reindex glossary definitions
        for obj in self.objectValues():
            if obj.portal_type in ('PloneGlossaryDefinition',):
                cat.catalog_object(obj)
    
registerType(PloneGlossary, PROJECTNAME)
