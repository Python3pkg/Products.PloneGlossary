"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import Globals
import StringIO
import os

# Zope imports
from Globals import package_home
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Acquisition import aq_base

# CMF imports
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import CMFCorePermissions
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

# PloneGlossary imports
from Products.PloneGlossary.config import GLOBALS, PROJECTNAME, PLONEGLOSSARY_TOOL
from Products.PloneGlossary.utils import text2words, find_word, escape_special_chars, encode_ascii
from Products.PloneGlossary.migration.Migrator import Migrator

_www = os.path.join(os.path.dirname(__file__), 'www')

class PloneGlossaryTool(PropertyManager, UniqueObject, SimpleItem):
    """Tool for PloneGlossary"""

    plone_tool = 1
    id = PLONEGLOSSARY_TOOL
    title = 'PloneGlossaryTool'
    meta_type = 'PloneGlossaryTool'
    
    _properties=(
        {'id':'title', 'type': 'string', 'mode':'w'},
        )
        
    _actions = ()
            
    manage_options=(PropertyManager.manage_options +\
                    SimpleItem.manage_options +\
                    ({ 'label' : 'Migrate',
                      'action' : 'manage_migration'},
                    )
                   )

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.ManagePortal, 'manage_migration')
    manage_migration = PageTemplateFile('manage_migration', _www)

    #                                                                                   #
    #                                Migrations management                              #
    #                                                                                   #

    
    security.declareProtected(CMFCorePermissions.ManagePortal, 'manage_migrate')
    def manage_migrate(self, REQUEST=None):
        """Migration script"""
        
        request = self.REQUEST
        options = {}
        options['dry_run'] = 0
        options['meta_type'] = 0
        stdout = StringIO.StringIO()
        
        if request is not None:
            options['dry_run'] = request.get('dry_run', 0)
            options['meta_type'] = request.get('meta_type', 'PloneGlossary')
        
        Migrator().migrate(self, stdout, options)
        
        if request is not None:
            message = "Migration completed."
            logs = stdout.getvalue()
            logs = '<br />'.join(logs.split('\r\n'))
            return self.manage_migration(self, manage_tabs_message = message, logs=logs)

    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, item, container):
        self.initProperties()

    security.declareProtected(CMFCorePermissions.ManagePortal, 'initProperties')
    def initProperties(self):
        """Init properties"""
        
        self.safeEditProperty(self, 'show_portlet', 1, data_type='boolean')
        self.safeEditProperty(self, 'highlight_content', 1, data_type='boolean')
        self.safeEditProperty(self, 'general_glossary_uids', 'getGlossaryUIDs', data_type='multiple selection', new_value=[])
        self.safeEditProperty(self, 'allowed_portal_types', 'getAvailablePortalTypes', data_type='multiple selection', new_value=['PloneGlossaryDefinition'])
        self.safeEditProperty(self, 'description_length', 0, data_type='int')
        self.safeEditProperty(self, 'description_ellipsis', '...', data_type='string')
        self.safeEditProperty(self, 'not_highlighted_tags', ['a', 'h1', 'input','textarea'], data_type='lines')
    
    security.declarePrivate('safeEditProperty')
    def safeEditProperty(self, obj, key, value, data_type='string', new_value=None):
        """ An add or edit function, surprisingly useful :) """
        
        if obj.hasProperty(key):
            for property in self._properties:
                if property['id'] == key:
                    property['data_type'] = data_type
                    if data_type in ('selection', 'multiple selection'):
                        property['select_variable'] = value
                    break
        else:
            obj._setProperty(key, value, data_type)
            
            if new_value is not None:
                obj._updateProperty(key, new_value)
    
    security.declarePublic('getAvailablePortalTypes')
    def getAvailablePortalTypes(self):
        """Returns available portal types"""
        
        portal_types = getToolByName(self, 'portal_types')
        return portal_types.listContentTypes()
    
    security.declarePublic('getAllowedPortalTypes')
    def getAllowedPortalTypes(self):
        """Returns allowed portal types.
        Allowed portal types can be highlighted."""
    
        return self.allowed_portal_types
    
    security.declarePublic('showPortlet')
    def showPortlet(self):
        """Returns true if you want to show glosssary portlet"""
        
        return self.show_portlet
    
    security.declarePublic('highlightContent')
    def highlightContent(self, obj):
        """Returns true if content must be highlighted"""
        
        portal_type = obj.getTypeInfo().getId()
        allowed_portal_types = self.getAllowedPortalTypes()
        
        if allowed_portal_types and portal_type not in allowed_portal_types:
            return False
        
        return self.highlight_content
    
    security.declarePublic('getGeneralGlossaryUIDs')
    def getGeneralGlossaryUIDs(self):
        """Returns glossary UIDs used to highlight content"""
        
        return self.general_glossary_uids
    
    security.declarePublic('getGeneralGlossaries')
    def getGeneralGlossaries(self):
        """Returns glossaries used to highlight content"""
        
        return self.getGlossaries(general_glossary_uids)
    
    security.declarePublic('getGlossaryUIDs')
    def getGlossaryUIDs(self):
        """Returns glossary UIDs defined on portal"""
        
        uid_cat = getToolByName(self, 'uid_catalog')
        brains = uid_cat(portal_type='PloneGlossary')
        return tuple([x.UID for x in brains])
    
    security.declarePublic('getGlossaries')
    def getGlossaries(self, glossary_uids=None): 
        """Returns glossaries defined on portal"""
        
        glossaries = []
        uid_cat = getToolByName(self, 'uid_catalog')
        mbtool = getToolByName(self, 'portal_membership')
        kwargs = {}
        if glossary_uids is not None:
            kwargs['UID'] = glossary_uids
        
        brains = uid_cat(portal_type='PloneGlossary', **kwargs)
        
        for brain in brains:
            obj = brain.getObject()
            
            if obj is None:
                continue
            
            # Check view permission
            has_view_permission = mbtool.checkPermission(CMFCorePermissions.View, obj) and mbtool.checkPermission(CMFCorePermissions.AccessContentsInformation, obj)
            if has_view_permission:
                glossaries.append(obj)
        
        return tuple(glossaries)
    
    # Make it private because this method doesn't check term security
    def _getGlossaryTermItems(self, glossary_uids):
        """Returns glossary terms as a list of dictionaries
        
        Item:
        - path -> term path
        - id -> term id
        - title -> term title
        - variants -> term variants
        - description -> term description
        - url -> term url
            
        @param glossary_uids: uids of glossary where we get terms
        """
        
        # Get glossaries
        glossaries = self.getGlossaries(glossary_uids)
        if not glossaries:
            return []
        
        # Get items
        items = []
        for glossary in glossaries:
            new_items = glossary._getGlossaryTermItems()
            items.extend(new_items)
        return tuple(items)
    
    security.declarePublic('getGlossaryTermItems')
    def getGlossaryTermItems(self, glossary_uids):
        """Returns the same list as _getGlossaryTermItems but check security.
        
        @param glossary_uids: Uids of glossary where we get term items"""
        
        # Get glossaries term items
        not_secured_term_items = self._getGlossaryTermItems(glossary_uids)
        
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
    
    security.declarePublic('getGlossaryTerms')
    def getGlossaryTerms(self, glossary_uids):
        """Returns term titles stored in glossaries.
        
        @param glossary_uids: Uids of glossary where we get term items"""
        
        # Get glossaries term items
        term_items = self.getGlossaryTermItems(glossary_uids)
        
        # Returns titles
        return [x['title'] for x in term_items]
    
    def _getObjectText(self, obj):
        """Returns all text of an object.
        
        If object is an AT content, get schema and returns all text fields.
        Otherwise returns SearchableText.
        
        @param obj: Content to analyse"""
        
        text = ''
        if hasattr(aq_base(obj), 'Schema'):
            schema = obj.Schema()
            
            # Loop on fields
            for field in schema.fields():
                if field.type in ('string', 'text',):
                    value = field.getRaw(obj)
                    
                    # Make sure value is a string
                    if type(value) == type(''):
                        text += value
        elif hasattr(aq_base(obj), 'SearchableText'):
            text = obj.SearchableText()

        return text
    
    # Make it private because this method doesn't check term security
    def _getObjectRelatedTermItems(self, obj, glossary_term_items):
        """Returns object terms in a specific structure
        
        Item:
        - terms -> object terms
        - path -> term path
        - id -> term id
        - title -> term title
        - variants -> term variants
        - description -> term description
        - url -> term url
        
        @param obj: object to analyse
        @param glossary_term_items: Glossary term items to check in the object text
        
        Variables starting with a are supposed to be in ASCII
        Variables starting with u are supposed to be in Unicode
        """
        
        charset = self._getSiteCharset()
        
        # Get obj properties
        obj_term_items = []
        ptype = obj.portal_type
        title = obj.title_or_id()
        utitle = title.decode(charset, "replace")
        atitle = encode_ascii(utitle)
        text = self._getObjectText(obj)
        utext = text.decode(charset, "replace")
        usplitted_text_terms = self._split(utext)
        atext = encode_ascii(utext)
        
        # Words to remove from terms to avoid recursion
        # For example, on a glossary definition itself, it makes no sense to
        # underline the defined word.
        aremoved_words = () 
        if ptype in ('PloneGlossaryDefinition',):
            aremoved_words = (atitle,)
        
        # Search glossary terms in text
        analyzed_terms = []
        for item in glossary_term_items:
            # Take into account the word and its variants
            terms = []
            item_title = item['title'] 
            item_variants = item['variants']
            
            if type(item_title) == type(''):
                terms.append(item_title)
            if type(item_variants) in (type([]), type(()), ):
                terms.extend(item_variants)
            
            # Loop on glossary terms and intersect with object terms 
            for term in terms:
                if term in analyzed_terms:
                    continue
                
                # Analyze term
                analyzed_terms.append(term)
                uterm = term.decode(charset, "replace")
                aterm = encode_ascii(uterm)
                if aterm in aremoved_words:
                    continue
                
                # Search the word in the text
                found_pos = find_word(aterm, atext)
                if not found_pos:
                    continue
    
                # Extract terms from obj text
                term_length = len(aterm)
                text_terms = []
                for pos in found_pos:
                    utext_term = utext[pos:(pos + term_length)]
                    
                    # FIX ME: Workaround for composed words. Works in 99%
                    # Check the word is not a subword but a real word composing the text
                    if not [x for x in self._split(utext_term) if x in usplitted_text_terms]:
                        continue
                    
                    # Encode the term and make sure there are no doublons
                    text_term = utext_term.encode(charset, "replace")
                    if text_term in text_terms:
                        continue
                    text_terms.append(text_term)
                
                if not text_terms:
                    continue
                
                # Append object term item
                new_item = item.copy()
                new_item['terms'] = text_terms
                obj_term_items.append(new_item)
            
        return obj_term_items
    
    
    security.declarePublic('getObjectRelatedTermItems')
    def getObjectRelatedTermItems(self, obj, glossary_term_items):
        """Returns the same list as _getObjectRelatedTermItems but check security.
        
        @param obj: object to analyse
        @param glossary_term_items: Glossary term items to check in the object text"""
        
        # Get glossaries term items
        not_secured_term_items = self._getObjectRelatedTermItems(obj, glossary_term_items)
        
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
    
    security.declarePublic('getObjectRelatedTerms')
    def getObjectRelatedTerms(self, obj, glossary_uids):
        """Returns glossary term titles found in object
        
        @param obj: Content to analyse and extract related glossary terms
        @param glossary_uids: if None tool will search all glossaries
        """
        
        # Get term definitions found in obj
        definitions = self.getObjectRelatedDefinitions(obj, glossary_uids)        
        
        # Returns titles
        return [x['title'] for x in definitions]
    
    
    security.declarePublic('getObjectRelatedDefinitions')
    def getObjectRelatedDefinitions(self, obj, glossary_uids):
        """Returns object term definitions get from glossaries.
        
        definition :
        - terms -> exact words in obj text
        - id -> term id
        - path -> term path
        - title -> term title
        - variants -> term variants
        - description -> term definitions
        - url -> term url
        
        @param obj: Content to analyse and extract related glossary terms
        @param glossary_uids: if None tool will search all glossaries
        """

        # Get glossary term items from the glossary
        # All terms are loaded in the memory as a list of dictionaries
        glossary_term_items = self._getGlossaryTermItems(glossary_uids)

        marked_definitions = []
        urls = {}
        # Search related definitions in glossary definitions
        for definition in self.getObjectRelatedTermItems(obj, glossary_term_items):
            if urls.has_key(definition['url']):
                # The glossary item is already going to be shown
                definition['show']=0
            else:
                # The glossary item is going to be shown
                urls[definition['url']]=1
                definition['show']=1
            marked_definitions.append(definition)
        return marked_definitions

    security.declarePublic('searchResults')
    def searchResults(self, glossary_uids, **search_args):
        """Returns brains from glossaries.
        glossary_uids: UIDs of glossaries where to search.
        search_args: Use index of portal_catalog."""
        
        # Get path of glossaries
        glossaries = self.getGlossaries(glossary_uids)
        paths = ['/'.join(x.getPhysicalPath()) for x in glossaries]
        ctool = getToolByName(self, 'portal_catalog')
        return ctool.searchResults(path=paths,
                                   portal_type='PloneGlossaryDefinition',
                                   **search_args)
    
    security.declarePublic('getAbcedaire')
    def getAsciiLetters(self):
        """Returns list of ascii letters in lower case"""
        
        return tuple([chr(x) for x in range(97,123)])
    
    security.declarePublic('getAbcedaire')
    def getAbcedaire(self, glossary_uids):
        """Returns abcedaire.
        glossary_uids: UIDs of glossaries used to build abcedaire"""
        
        terms = self.getGlossaryTerms(glossary_uids)
        letters = []
        
        for term in terms:
            letter = term[0:1].lower()
            if letter not in letters:
                letters.append(letter)
        
        # Sort alphabetically
        letters.sort()
        
        return tuple(letters)
        
    security.declarePublic('getAbcedaireBrains')
    def getAbcedaireBrains(self, glossary_uids, letters):
        """Returns brains from portal_catalog.
        glossary_uids: UIDs of glossaries used to build abcedaire.
        letters: beginning letters of terms to search"""
        
        abcedaire_brains = []
        brains = self.searchResults(glossary_uids)
        
        for brain in brains:
            letter = brain.Title[0:1].lower()
            if letter in letters:
                abcedaire_brains.append(brain)
        
        # Sort alphabetically
        def cmp_alpha(a, b):
            return cmp(a.Title, b.Title)
        
        abcedaire_brains.sort(cmp_alpha)
        
        return abcedaire_brains

    security.declarePublic('truncateDescription')
    def truncateDescription(self, text):
        """Truncate definition using tool properties"""
        
        max_length = self.description_length
        site_charset = self._getSiteCharset()
        text = text.decode(site_charset, "replace")
        text = text.strip()
        
        if max_length > 0 and len(text) > max_length:
            ellipsis = self.description_ellipsis
            text = text[:max_length]
            text = text.strip()
            text = '%s %s' %(text, ellipsis)
        
        text = text.encode(site_charset, "replace")
        
        return text 

    security.declarePublic('escape')
    def escape(self, text):
        """Returns escaped text."""
        
        return escape_special_chars(text)
    
    def _getSiteCharset(self):
        """Returns site charset"""
        
        # Get site charset
        ptool = getToolByName(self, 'portal_properties')
        return ptool.site_properties.default_charset
        
    def _split(self, text, removed_words=()):
        """Split unicode text into tuple of unicode terms
        
        @param text: unicode text to split
        @param remove_words: words to remove from the split result"""
        
        return tuple([x for x in text2words(text) if len(x) > 1 and x not in removed_words])

InitializeClass(PloneGlossaryTool)
