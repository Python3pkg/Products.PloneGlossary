# -*- coding: utf-8 -*-
##
# Copyright (C) 2007 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file LICENSE. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""
Unit test main script
"""

from Products.PloneGlossary.tests import PloneGlossaryTestCase
from Products.PloneGlossary.utils import html2text
from Products.PloneGlossary.utils import find_word
from Products.PloneGlossary.utils import encode_ascii

from Products.PloneGlossary.utils import LOG


class TestPloneGlossary(PloneGlossaryTestCase.PloneGlossaryTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.glossary = self.addGlossary(
            self.portal,
            'General',
            ('Sport', 'Tennis \t\n', 'Open source'))
        self.logout()

    def testGetGlossaries(self):
        self.loginAsPortalOwner()
        medical_glossary = self.addGlossary(
            self.portal, 'Medical', ('ADN', 'Bone', 'Heart'))
        uids = []
        uids.append(self.glossary.UID())
        uids.append(medical_glossary.UID())
        uids.sort()

        # Test PloneGlossaryTool->getGlossaryUIDs
        glossary_uids = sorted(self.glossary_tool.getGlossaryUIDs())
        self.assertEquals(glossary_uids, uids)

        # Test PloneGlossaryTool->getGlossaries
        glossary_uid = self.glossary.UID()
        glossaries = self.glossary_tool.getGlossaries(
            glossary_uids=[glossary_uid])
        glossary = glossaries[0]
        self.assertEquals(glossary.UID(), glossary_uid)

        glossary_uids = [x.UID() for x in self.glossary_tool.getGlossaries()]
        glossary_uids.sort()
        self.assertEquals(glossary_uids, uids)
        self.logout()

    def testGetAvailableGlossaryMetaTypes(self):
        self.loginAsPortalOwner()
        tool = self.glossary_tool
        available_metatypes = tool.getAvailableGlossaryMetaTypes()
        glossary_metatypes = tool.glossary_metatypes

        # test available metatypes, base glossary selected by default
        self.assertEquals(available_metatypes,
                          ('PloneGlossary', 'ExampleGlossary'))
        self.assertEquals(glossary_metatypes, ('PloneGlossary',))

        # test : only selected metatypes are returned by getGlossaryUIDs
        glossary = self.glossary
        glossaryuid = glossary.UID()
        exampleglossary = self.addExampleGlossary(
            self.portal,
            'Example',
            ('Sport', 'Tennis', 'Open source'))
        exampleuid = exampleglossary.UID()

        # test :
        glossary_uids = sorted(self.glossary_tool.getGlossaryUIDs())
        self.assertEquals(glossary_uids, [glossaryuid])

        # test : add a glossary type
        tool.glossary_metatypes = ('PloneGlossary', 'ExampleGlossary')
        glossary_uids = list(self.glossary_tool.getGlossaryUIDs())
        glossary_uids.sort()
        uids = [glossaryuid, exampleuid]
        uids.sort()
        self.assertEquals(glossary_uids, uids)
        LOG.info("testGetAvailableGlossaryMetaTypes passed")
        self.logout()

    def testGetGeneralGlossaryUIDs(self):
        self.loginAsPortalOwner()
        medical_glossary = self.addGlossary(self.portal, 'Medical',
                                            ('ADN', 'Bone', 'Heart'))
        all_uids = []
        all_uids.append(self.glossary.UID())
        all_uids.append(medical_glossary.UID())
        all_uids.sort()
        general_glossaries_uids = sorted(
            self.glossary_tool.getGeneralGlossaryUIDs())
        self.assertEquals(general_glossaries_uids, all_uids)

        self.glossary_tool.general_glossary_uids = (medical_glossary.UID(),)
        general_glossaries_uids = self.glossary_tool.getGeneralGlossaryUIDs()
        self.assertEquals(list(general_glossaries_uids),
                          [medical_glossary.UID()])

    def testTextRelatedTerms(self):
        self.loginAsPortalOwner()
        gtool = self.glossary_tool
        glossary_uids = gtool.getGlossaryUIDs()
        glossary_term_items = gtool._getGlossaryTermItems(glossary_uids)

        terms = sorted(self.glossary_tool._getTextRelatedTermItems(
            "Le tennis est un sport", glossary_term_items))
        terms = [t['title'] for t in terms]
        self.assertEquals(terms, ['Sport', 'Tennis \t\n'])

        terms = list(self.glossary_tool._getTextRelatedTermItems(
            "Le tennis est un sport", glossary_term_items,
            excluded_terms=('Tennis',)))

        terms.sort()
        terms = [t['title'] for t in terms]
        self.assertEquals(terms, ['Sport'])

    def testObjectRelatedTerms(self):
        self.loginAsPortalOwner()
        # Add french document
        doc = self.addFrenchDocument(
            self.portal,
            self.encodeInSiteCharset('Sport fran\xe7ais'))
        glossary_uids = self.glossary_tool.getGlossaryUIDs()
        terms = sorted(self.glossary_tool.getObjectRelatedTerms(
            doc, glossary_uids))
        result = ['Sport']
        self.assertEquals(terms, result)

        # Test terms using 2 words like "open source"
        doc = self.addDocument(
            self.portal,
            self.encodeInSiteCharset(
                'English documentation'),
            self.encodeInSiteCharset('This is an open source'),)
        terms = list(self.glossary_tool.getObjectRelatedTerms(
            doc, glossary_uids))
        terms.sort()
        result = ['Open source']
        self.assertEquals(terms, result)

        self.logout()

    def testObjectRelatedDefinitions(self):
        self.loginAsPortalOwner()
        # Add french document
        doc = self.addFrenchDocument(
            self.portal,
            self.encodeInSiteCharset('Sport fran\xe7ais'))

        # no glossary_uid
        result = self.glossary_tool.getObjectRelatedDefinitions(doc, ())
        self.assertEquals(result, [])

        # test normal
        glossary_uids = self.glossary_tool.getGlossaryUIDs()
        definitions = list(self.glossary_tool.getObjectRelatedDefinitions(
            doc, glossary_uids))
        self.assertEquals(len(definitions), 1)
        definition = definitions[0]
        self.assertEquals(definition['url'],
                          'http://nohost/plone/general/sport')
        self.assertEquals(definition['description'], 'Definition of term')
        self.assertEquals(definition['variants'], ())
        self.assertEquals(definition['id'], 'sport')
        self.assertEquals(definition['title'], 'Sport')
        self.logout()

    def testGlossaryTerms(self):
        self.loginAsPortalOwner()
        glossary_uids = self.glossary_tool.getGlossaryUIDs()
        terms = sorted(self.glossary_tool.getGlossaryTerms(glossary_uids))
        result = ['Open source', 'Sport', 'Tennis \t\n']
        self.assertEquals(terms, result)
        self.logout()

    def testGetAbcedaire(self):
        """We should have the 1st letters of all words (merged)"""
        self.loginAsPortalOwner()
        abcedaire = self.glossary_tool.getAbcedaire([self.glossary.UID()])
        result = ('o', 's', 't')
        self.assertEquals(abcedaire, result)

        brains = self.glossary_tool.getAbcedaireBrains([self.glossary.UID()],
                                                       letters=['s'])
        self.assertEquals(len(brains), 1)
        brain = brains[0]
        self.assertEquals(brain.Title, 'Sport')
        self.logout()

    def testSearchResults(self):
        self.loginAsPortalOwner()
        brains = self.glossary_tool.searchResults(
            [self.glossary.UID()], Title='Sport')
        self.assertEquals(len(brains), 1)
        brain = brains[0]
        self.assertEquals(brain.Title, 'Sport')
        self.logout()

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
        self.glossary = self.addGlossary(
            self.portal,
            'Produits laitiers',
            ('Lait',
             'Beurre',
             'Fromage',
             'Crème',
             'Desserts lactés'))
        # Variants of yaourt are yoghourt and yogourt
        self.addGlossaryDefinition(
            self.glossary,
            title='Yaourt',
            definition='Lait caillé ayant subi une fermentation acide.',
            variants=('Yaourts',
                      'Yoghourt',
                      'Yoghourts \t',
                      'yogourt',
                      'yogourts'))
        # Variants of fruits, to test white space in variants.  But
        # white space is stripped on save there.  So not much
        # interesting happens.
        self.addGlossaryDefinition(
            self.glossary,
            title='Fruits',
            definition='Commes des légumes, mais un peut autre.',
            variants=('Apples',
                      'Fraises \t',
                      'Framboises'))

        doc = self.addDocument(
            self.portal,
            "Dessert",
            ("Notre chef vous propose des fraises au yaourt et des yoghourts "
             "à la vanille."))

        brains = self.glossary_tool.searchResults([self.glossary.UID()],
                                                  SearchableText='Yoghourt')
        self.assertEquals(brains[0].Title, 'Yaourt')
        brains = self.glossary_tool.searchResults([self.glossary.UID()],
                                                  SearchableText='Fraises')
        self.assertEquals(brains[0].Title, 'Fruits')

        definitions = self.portal.portal_glossary.getObjectRelatedDefinitions(
            doc, glossary_uids=[self.glossary.UID()])
        self.assertEquals(len(definitions), 3)
        definition = definitions[0]
        self.assertEquals(definition['terms'], ['yaourt'])
        self.assertEquals(definition['show'], 1)
        definition = definitions[1]
        self.assertEquals(definition['terms'], ['yoghourts'])
        self.assertEquals(definition['show'], 0)
        definition = definitions[2]
        self.assertEquals(definition['terms'], ['fraises'])
        self.assertEquals(definition['show'], 1)

    def testEncoding(self):
        """Test encoding"""
        self.loginAsPortalOwner()
        # Add glossary
        self.glossary = self.addGlossary(
            self.portal,
            'Parfums Femme Chanel',
            ('Lancôme : Ô Oui',
             "Dior : J´Adore",
             'Cerruti 1881 pour Femme',
             ))
        # Variants of yaourt are yoghourt and yogourt
        self.addGlossaryDefinition(
            self.glossary,
            title='Chanel N° 5',
            definition=("Un bouquet de fleurs abstraites d'une "
                        "indéfinissable féminité."),
            variants=('N° 5', ))
        doc = self.addDocument(
            self.portal,
            "Le parfum de ma mère!",
            ("Alors pour vous dire, une très grande histoire d'amour!! et ce "
             "n'est pas par hasard que ça fait maintenant plus de 80ans que "
             "Chanel N° 5 se vend!"))

        brains = self.glossary_tool.searchResults([self.glossary.UID()],
                                                  SearchableText='N° 5')
        self.assertEquals(brains[0].Title, 'Chanel N° 5')

        definitions = self.portal.portal_glossary.getObjectRelatedDefinitions(
            doc, glossary_uids=[self.glossary.UID()])
        definition = definitions[0]
        self.assertEquals(definition['terms'], ['Chanel N° 5'])
        self.assertEquals(definition['show'], 1)

    def testEncodeAscii(self):
        """Test encode_ascii function from utils modules"""

        utext = 'Ellipsis\u2026'
        atext = encode_ascii(utext)
        self.assertEquals(len(utext), len(atext))
        self.assertEquals(atext, "ellipsis.")

    def testHTML2Text(self):
        """Test correct splitting of HTML"""
        text = html2text("<div>line1\r\nline2</div>")
        self.assertEquals(text, "line1 line2")
        text = html2text("<div>line1\r\n line2</div>")
        self.assertEquals(text, "line1 line2")
        text = html2text("<div>line1 \r\n line2</div>")
        self.assertEquals(text, "line1 line2")
        text = html2text("<div>line1 \r \n line2</div>")
        self.assertEquals(text, "line1 line2")
        text = html2text("<div><ul><li>Seleção campeã!</li></ul></div>")
        self.assertEquals(text, "- Seleção campeã!".encode("utf-8"))
        text = html2text(
            "<div><ul><li>Sele&ccedil;&atilde;o campe&atilde;!</li>"
            "</ul></div>")
        self.assertEquals(text, "- Seleção campeã!".encode("utf-8"))
        text = html2text(
            "<div><ul><li>Sele&#231;&#227;o campe&#227;!</li></ul></div>")
        self.assertEquals(text, "- Seleção campeã!".encode("utf-8"))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneGlossary))
    return suite
