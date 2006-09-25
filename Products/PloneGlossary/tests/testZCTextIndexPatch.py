# -*- coding: utf-8 -*-
"""
$Id$
"""
from common import *

class TestZCTextIndexPatch(PloneGlossaryTestCase.PloneGlossaryTestCase):

    def testDefaultConfig(self):

        #This test is here to prevent changing default behaviour by accident:
        # we don't want to release or commit with patching enabled.
        # That's defensive
        from Products.PloneGlossary.config import PATCH_ZCTextIndex
        from Products.PloneGlossary.config import INDEX_SEARCH_GLOSSARY

        self.assertEquals(PATCH_ZCTextIndex, False)
        self.assertEquals(INDEX_SEARCH_GLOSSARY, ('SearchableText',))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestZCTextIndexPatch))
    return suite

if __name__ == '__main__':
    framework()
