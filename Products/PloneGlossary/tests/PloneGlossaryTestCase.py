# -*- coding: utf-8 -*-
"""
$Id$
"""

# Python imports
import re
import os
import time
import Globals

# Zope imports
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager

# CMF imports
from Products.CMFCore.utils import getToolByName

# Plone imports
from Products.PloneTestCase import PloneTestCase

# Globals
portal_name = 'portal'
portal_owner = 'portal_owner'
default_user = PloneTestCase.default_user
default_password = PloneTestCase.default_password

class PloneGlossaryTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
        
        # Configure tool
        self.glossary_tool = getToolByName(self.portal, 'portal_glossary')
        self.mb_tool = getToolByName(self.portal, 'portal_membership')
        prop_tool = getToolByName(self.portal, 'portal_properties')
        self.site_charset = prop_tool.site_properties.default_charset
        
    def beforeTearDown(self):
        """Remove all the stuff again.
        """
        
        pass
    
    def loginAsPortalOwner(self):
        '''Use if you need to manipulate an article as member.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)
    
    def encodeInSiteCharset(self, text):
        """Text is unicode text"""
        
        return text.encode(self.site_charset)
    
    def buildPrettyId(self, title):
        """Returns pretty id from title"""
        
        regexp = re.compile(r'[^ a-z]')
        pretty_id = regexp.sub('', title.lower())
        return pretty_id
    
    def addDocument(self, container, doc_title, doc_text):
        """Add document in container"""
        
        doc_id = self.buildPrettyId(doc_title)
        
        container.invokeFactory(
            type_name='Document',
            id=doc_id,
            title=doc_title,
            text=doc_text)
            
        return getattr(container, doc_id)
    
    def addFrenchDocument(self, container, doc_title):
        """Add french document in container"""
        
        return self.addDocument(container, doc_title, self.getFrenchText())
    
    def addEnglishDocument(self, container, doc_title):
        """Add english document in container"""
        
        return self.addDocument(container, doc_title, self.getEnglishText())
    
    def getFrenchText(self):
        """Returns french text"""
        
        return self.encodeInSiteCharset(u"""D\xe9finition d'un terme.""")
    
    def getEnglishText(self):
        """Returns french text"""
        
        return self.encodeInSiteCharset(u"""Term definition.""")
    
    def addGlossaryDefinition(self, glossary, title, definition=None, variants=()):
        """Add new glossary definition in a glossary"""
        
        if definition is None:
            definition = self.encodeInSiteCharset(u'Definition of term')

        id = self.buildPrettyId(title)
        glossary.invokeFactory(
            type_name='PloneGlossaryDefinition',
            id=id,
            title=title,
            definition=definition,
            variants=variants)
    
        term = getattr(glossary, id)
        return term
    
    def addGlossary(self, container, glossary_title, term_titles):
        """Add glossary in container with definitions"""
        
        # Add glossary
        glossary_id = self.buildPrettyId(glossary_title)
        container.invokeFactory(
            type_name='PloneGlossary',
            id=glossary_id,
            title=glossary_title)
            
        glossary = getattr(container, glossary_id)
        
        # Add terms
        for term_title in term_titles:
            self.addGlossaryDefinition(glossary, term_title)
        
        return glossary
            

# Install PloneGlossary
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PloneGlossary')

# Setup Plone site
PloneTestCase.setupPloneSite(products=['Archetypes', 'PloneGlossary'])
