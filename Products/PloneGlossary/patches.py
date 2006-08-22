# -*- coding: utf-8 -*-
## PloneGlossary monkeypatches
## 
## Copyright (C) 2006 Ingeniweb

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

from Products.CMFCore.utils import getToolByName

from config import PATCH_ZCTextIndex, INDEX_SEARCH_GLOSSARY, \
     PORTAL_TYPES_TO_SKIP
from config import PLONEGLOSSARY_TOOL

# Patch ZCTextIndex.index_object: we add synonyms of glossary items/variants
# found in the text. A search query on a variant (not present in original text)
# will also return the document.
from Products.PluginIndexes.common import safe_callable
from Products.ZCTextIndex.ZCTextIndex import ZCTextIndex

def indexObjectsWidthSynonyms(self, documentId, obj, threshold=None):
    """Wrapper for  index_doc()  handling indexing of multiple attributes.

    Enter the document with the specified documentId in the index
    under the terms extracted from the indexed text attributes,
    each of which should yield either a string or a list of
    strings (Unicode or otherwise) to be passed to index_doc().

    Monkey Patch from PloneGlossary: add synonyms to indexed text
    """
    # XXX We currently ignore subtransaction threshold
    # needed for backward compatibility
    try: fields = self._indexed_attrs
    except: fields  = [ self._fieldname ]

    res = 0
    all_texts = []
    for attr in fields:
        text = getattr(obj, attr, None)
        if text is None:
            continue
        if safe_callable(text):
            text = text()
        if text is None:
            continue
        if text:
            if isinstance(text, (list, tuple, )):
                all_texts.extend(text)
            else:
                all_texts.append(text)

    # Check that we're sending only strings
    all_texts = filter(lambda text: isinstance(text, basestring), \
                       all_texts) 
    
    if all_texts:

        # lookup glossary terms
        if (self.getId() in INDEX_SEARCH_GLOSSARY
            and obj.portal_type not in PORTAL_TYPES_TO_SKIP):
            
            supp_items = []
            gtool = getToolByName(self, PLONEGLOSSARY_TOOL)
            glossary_uids = gtool.getGeneralGlossaryUIDs()
            all_term_items = gtool._getGlossaryTermItems(glossary_uids)
            for text in all_texts:
                terms = gtool._getTextRelatedTermItems(text, all_term_items)
                flat_list = []
                for t in terms:
                    flat_list.extend((t['title'],) + t['variants'])
                    
                supp_items.extend(flat_list)
            all_texts.extend(supp_items)

        return self.index.index_doc(documentId, all_texts)
    return res

if PATCH_ZCTextIndex:
    ZCTextIndex.index_object = indexObjectsWidthSynonyms
