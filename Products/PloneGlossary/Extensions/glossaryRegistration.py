from Products.CMFCore.utils import getToolByName
from Products.PloneGlossary.config import PLONEGLOSSARY_TOOL

def registerGlossary(context, glossaryClass, out):
    pgtool = getToolByName(context, PLONEGLOSSARY_TOOL)
    registered_metatypes = pgtool.available_glossary_metatypes
    new_glossary_metatype = glossaryClass.meta_type
    if not new_glossary_metatype in registered_metatypes:
        pgtool.available_glossary_metatypes += (new_glossary_metatype,)
        out.write("%s glossary registered" % new_glossary_metatype)