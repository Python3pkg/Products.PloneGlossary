## -*- coding: utf-8 -*-
## Copyright (C) 2007 Ingeniweb

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


"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# CMF imports
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:
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
