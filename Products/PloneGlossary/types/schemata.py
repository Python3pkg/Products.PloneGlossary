# -*- coding: utf-8 -*-
"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# CMF imports
from Products.CMFCore import CMFCorePermissions

# Archetypes import
from Products.Archetypes.public import *

from Products.ATContentTypes.configuration import zconf

# PloneGlossary schema
PloneGlossarySchema = BaseSchema.copy()
PloneGlossarySchema['description'].schemata = 'default'

# PloneGlossaryDefinition schema
PloneGlossaryDefinitionSchema = BaseSchema.copy() + Schema((
    StringField(
        'title',
        required=True,
        searchable=True,
        default='',
        accessor='Title',
        widget=StringWidget(
            label = "Term",
            label_msgid="label_glossary_term",
            description = "Enter the term to be defined.",
            description_msgid = "help_glossary_term",
            visible={'view' : 'invisible'},
            i18n_domain="ploneglossary"),
        ),
    LinesField(
        'variants',
        required=False,
        searchable=True,
        default=(),
        widget=LinesWidget(
            label = "Variants",
            label_msgid="label_glossary_variants",
            description = "Enter the variants of the term, one per line.",
            description_msgid = "help_glossary_variants",
            visible={'view' : 'invisible'},
            i18n_domain="ploneglossary"),
        ),
    TextField(
        'definition',
        required=True,
        searchable=True,
        default_content_type = zconf.ATDocument.default_content_type,
        default_output_type = 'text/x-html-safe',
        allowable_content_types = zconf.ATDocument.allowed_content_types,
        widget = RichWidget(
            label = "Body text",
            label_msgid = "label_glossary_definition_text",
            description = "Enter the body text.",
            description_msgid = "help_glossary_definition_text",
            rows = 25,
            i18n_domain = "ploneglossary"),
        ),

    ))

# Hide description. It is generated dynamically
#PloneGlossaryDefinitionSchema['description'].widget.visible = {'view' : '
#visible', 'edit' : 'invisible'}
