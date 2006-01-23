##############################################################################
#
# Copyright (c) 2006 Ingeniweb SARL
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""PloneGlossary migration module
$Id: $
"""
__author__ = ''
__docformat__ = 'restructuredtext'

# Python imports
import sys

# Zope imports
from OFS.Image import File

# Archetypes imports
from Products.Archetypes.interfaces.base import IBaseUnit

# CMF imports
from Products.CMFCore.utils import getToolByName

class Migrator:
    """Migration class
    """
    def migrate1_2_to_1_3(self, portal, glossary_brains, stdout, options):
        """Migrate PloneGlossary 1.2 to 1.3
           Updates Catalogs contained in Glossaries if the getVariants index
           is not present.
        """

        dry_run = options.get('dry_run', False)

        if stdout is None:
            stdout = sys.stdout

        if dry_run:
            stdout.write('Results of the <strong>dry run</strong>:\r\n\r\n')

        stdout.write('Migrate PloneGlossary 1.2 to 1.3\r\n')

        nb_glossaries = 0
        already = 0

        stdout.write("There are %d Glossary objects.\r\n" % len(glossary_brains))

        for glossary_brain in glossary_brains:
            glossary=glossary_brain.getObject()
            glossary_catalog=glossary.getCatalog()

            # Check if it has not been done before
            if 'getVariants' in glossary_catalog.indexes():
                already += 1
                continue

            # This is a glossary from 1.2
            nb_glossaries += 1

            # Dry run: we simulate
            if not dry_run:
                # Update catalog
                stdout.write("Updating Catalog '%s'.\r\n" % glossary.absolute_url())
                if "getVariants" in glossary_catalog.indexes():
                    pass
                else:
                    glossary_catalog.addIndex("getVariants", "KeywordIndex")
                    glossary_catalog.manage_reindexIndex(ids=["getVariants",])
                if "getVariants" in glossary_catalog.schema():
                    pass
                else:
                    glossary_catalog.addColumn("getVariants")

                # Try to remove the glossary from live memory
                glossary = None

        if stdout is not None:
            if dry_run:
                stdout.write('%s glossaries would have been migrated.\r\n' % nb_glossaries)
            else:
                stdout.write('%s glossaries migrated.\r\n' % nb_glossaries)
            stdout.write('%s glossaries were already migrated.\r\n' % already)
            stdout.write('Migration from PloneGlossary 1.2 to 1.3 finished.\r\n')

    def migrate(self, portal, stdout=None, options={}):
        ctool = getToolByName(portal, 'portal_catalog')
        glossary_brains = ctool(meta_type=options['meta_type'])
        self.migrate1_2_to_1_3(portal, glossary_brains, stdout, options)
        glossary_brains = None
