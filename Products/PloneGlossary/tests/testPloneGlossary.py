# -*- coding: utf-8 -*-
"""
$Id$
"""

from common import *

class TestPloneGlossary(PloneGlossaryTestCase.PloneGlossaryTestCase):
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.glossary = self.addGlossary(self.portal, 
                                         u'General',
                                         (u'Sport', u'Tennis', u'Open source'))
        self.logout()

    def testGetGlossaries(self):
        self.loginAsPortalOwner()
        medical_glossary = self.addGlossary(self.portal, u'Medical', (u'ADN', u'Bone', u'Heart'))
        uids = []
        uids.append(self.glossary.UID())
        uids.append(medical_glossary.UID())
        uids.sort()
        
        # Test PloneGlossaryTool->getGlossaryUIDs
        glossary_uids = list(self.glossary_tool.getGlossaryUIDs())
        glossary_uids.sort()
        self.assertEquals(glossary_uids, uids)
        
        # Test PloneGlossaryTool->getGlossaries
        glossary_uid = self.glossary.UID()
        glossaries = self.glossary_tool.getGlossaries(glossary_uids=[glossary_uid])
        glossary = glossaries[0]
        self.assertEquals(glossary.UID(), glossary_uid)
        
        
        glossary_uids = [x.UID() for x in self.glossary_tool.getGlossaries()]
        glossary_uids.sort()
        self.assertEquals(glossary_uids, uids)
        self.logout()

    def testObjectRelatedTerms(self):
        self.loginAsPortalOwner()
        # Add french document
        doc = self.addFrenchDocument(self.portal, \
            self.encodeInSiteCharset(u'Sport fran\xe7ais'))
        glossary_uids = self.glossary_tool.getGlossaryUIDs()
        terms = list(self.glossary_tool.getObjectRelatedTerms(doc, glossary_uids))
        terms.sort()
        result = ['Sport']
        self.assertEquals(terms, result)
        
        # Test terms using 2 words like "open source"
        doc = self.addDocument(self.portal, \
            self.encodeInSiteCharset(u'English documentation'),
            self.encodeInSiteCharset(u'This is an open source'),)
        terms = list(self.glossary_tool.getObjectRelatedTerms(doc, glossary_uids))
        terms.sort()
        result = ['Open source']
        self.assertEquals(terms, result)
        
        self.logout()

    def testObjectRelatedDefinitions(self):
        self.loginAsPortalOwner()
        # Add french document
        doc = self.addFrenchDocument(self.portal, \
            self.encodeInSiteCharset(u'Sport fran\xe7ais'))
        glossary_uids = self.glossary_tool.getGlossaryUIDs()
        definitions = list(self.glossary_tool.getObjectRelatedDefinitions(doc, glossary_uids))
        self.assertEquals(len(definitions), 1)
        definition = definitions[0]
        self.assertEquals(definition['url'], 'http://nohost/plone/general/sport')
        self.assertEquals(definition['description'], u'Definition of term')
        self.assertEquals(definition['variants'], ())
        self.assertEquals(definition['id'], 'sport')
        self.assertEquals(definition['title'], u'Sport')
        self.logout()

    def testGlossaryTerms(self):
        self.loginAsPortalOwner()
        glossary_uids = self.glossary_tool.getGlossaryUIDs()
        terms = list(self.glossary_tool.getGlossaryTerms(glossary_uids))
        terms.sort()
        result = ['Open source', 'Sport', 'Tennis']
        self.assertEquals(terms, result)
        self.logout()

    def testGetAbcedaire(self):
        abcedaire = self.glossary_tool.getAbcedaire([self.glossary.UID()])
        result = ('o', 's', 't')
        self.assertEquals(abcedaire, result)
        
        brains = self.glossary_tool.getAbcedaireBrains([self.glossary.UID()], letters=['s'])
        self.assertEquals(len(brains), 1)
        brain = brains[0]
        self.assertEquals(brain.Title, 'Sport')
    
    def testSearchResults(self):
        brains = self.glossary_tool.searchResults([self.glossary.UID()], Title='Sport')
        self.assertEquals(len(brains), 1)
        brain = brains[0]
        self.assertEquals(brain.Title, 'Sport')

    def testFindWord(self):
        """Test find_word function in utils"""

        # The text is the word
        word = "ete"
        text = "ete"
        result = find_word(word, text)
        expected_result = (0,)
        self.assertEquals(result, expected_result)
        
        # Many words
        text = "l'ete ou ete"
        result = find_word(word, text)
        expected_result = (2, 9,)
        self.assertEquals(result, expected_result)

    def testVariants(self):
        """Test variants"""
        self.loginAsPortalOwner()
        # Add glossary
        self.glossary = self.addGlossary(self.portal, 
                                         u'Produits laitiers',
                                         (u'Lait',
                                          u'Beurre',
                                          u'Fromage',
                                          u'Crème',
                                          u'Desserts lactés'))
        # Variants of yaourt are yoghourt and yogourt
        self.addGlossaryDefinition(self.glossary,
                                  title=u'Yaourt',
                                  definition=u'Lait caillé ayant subi une fermentation acide.',
                                  variants=(u'Yaourts',
                                            u'Yoghourt',
                                            u'Yoghourts',
                                            u'yogourt',
                                            u'yogourts'))

        doc = self.addDocument(self.portal,
                               "Dessert",
                               "Notre chef vous propose des fraises au yaourt et des yoghourts à la vanille.")

        brains = self.glossary_tool.searchResults([self.glossary.UID()],
                                                  SearchableText='Yoghourt')
        self.assertEquals(brains[0].Title, 'Yaourt')
        
        definitions = self.portal.portal_glossary.getObjectRelatedDefinitions(doc, glossary_uids=None)
        definition= definitions[0]
        self.assertEquals(definition['terms'],['yaourt'])
        self.assertEquals(definition['show'],1)
        definition= definitions[1]
        self.assertEquals(definition['terms'],['yoghourts'])
        self.assertEquals(definition['show'],0)

    def testEncoding(self):
        """Test encoding"""
        self.loginAsPortalOwner()
        # Add glossary
        self.glossary = self.addGlossary(self.portal, 
                                         u'Parfums Femme Chanel',
                                         (u'Lancôme : Ô Oui',
                                          u"Dior : J´Adore",
                                          u'Cerruti 1881 pour Femme',
                                         ))
        # Variants of yaourt are yoghourt and yogourt
        self.addGlossaryDefinition(self.glossary,
                                  title=u'Chanel N° 5',
                                  definition=u"Un bouquet de fleurs abstraites d'une indéfinissable féminité.",
                                  variants=(u'N° 5',),)
        doc = self.addDocument(self.portal,
                               "Le parfum de ma mère!",
                               "Alors pour vous dire, une très grande histoire d'amour!! et ce n'est pas par hasard que ça fait maintenant plus de 80ans que Chanel N° 5 se vend!")
        
        brains = self.glossary_tool.searchResults([self.glossary.UID()],
                                                  SearchableText='N° 5')
        self.assertEquals(brains[0].Title, 'Chanel N° 5')
        
        definitions = self.portal.portal_glossary.getObjectRelatedDefinitions(doc, glossary_uids=None)
        definition= definitions[0]
        self.assertEquals(definition['terms'],['Chanel N° 5'])
        self.assertEquals(definition['show'],1)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneGlossary))
    return suite

if __name__ == '__main__':
    framework()
