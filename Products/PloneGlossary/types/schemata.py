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

# PloneGlossary schema
PloneGlossarySchema = BaseSchema.copy()

# PloneGlossaryDefinition schema
PloneGlossaryDefinitionSchema = BaseSchema.copy() + Schema((
    StringField(
        'title',
        required=True,
        searchable=True,
        default='',
        accessor='Title',
        widget=StringWidget(
            label = "Entry",
            label_msgid="label_glossary_title",
            description = "Enter the title's entry.",
            description_msgid = "help_glossary_title",
            visible={'view' : 'invisible'},
            i18n_domain="ploneglossary"),
        ),
    TextField(
        'definition',
        required=True,
        searchable=True,
        default_content_type = 'text/html',
        default_output_type = 'text/html',
        allowable_content_types = ('text/html',),
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
PloneGlossaryDefinitionSchema['description'].widget.visible = {'view' : 'visible', 'edit' : 'invisible'}
