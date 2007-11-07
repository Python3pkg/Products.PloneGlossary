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


import os
from copy import deepcopy

from zope.interface import implements


# Archetypes imports
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *


from Products.PloneGlossary.types.PloneGlossary\
        import PloneGlossary as PloneGlossary
from Products.PloneGlossary.types.PloneGlossaryDefinition \
        import PloneGlossaryDefinition as PloneGlossaryDefinition

from Products.PloneGlossary.interfaces import (IPloneGlossary,
                                               IPloneGlossaryDefinition)

from Products.PloneGlossary.config import \
     PROJECTNAME, \
     DEBUG, \
     INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE

ExampleGlossaryActions = deepcopy(PloneGlossary.actions)
ExampleGlossarySchema = PloneGlossary.schema.copy()


class ExampleGlossary(PloneGlossary):
    """ExampleGlossary"""
    
    implements(IPloneGlossary)
    
    definition_types = ('ExampleGlossaryDefinition',)
    
    portal_type = meta_type = 'ExampleGlossary'
    archetype_name = 'Glossary'
    schema = ExampleGlossarySchema
    actions = ExampleGlossaryActions
    allowed_content_types = definition_types
    
    
ExampleGlossaryDefinitionActions = deepcopy(PloneGlossaryDefinition.actions)
ExampleGlossaryDefinitionSchema = PloneGlossaryDefinition.schema.copy()


class ExampleGlossaryDefinition(PloneGlossaryDefinition):
    """ExamplePloneGlossaryDefinition"""
    
    implements(IPloneGlossaryDefinition)
    
    portal_type = meta_type = 'ExampleGlossaryDefinition'
    archetype_name = 'Glossary definition'
    schema =  ExampleGlossaryDefinitionSchema
    actions = ExampleGlossaryDefinitionActions

if DEBUG or os.environ.get(INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE):
    registerType(ExampleGlossary, PROJECTNAME)
    registerType(ExampleGlossaryDefinition, PROJECTNAME)

