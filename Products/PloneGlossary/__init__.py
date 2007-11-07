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

# Python imports
import sys
import logging
from Globals import package_home

# CMF imports
from Products.CMFCore.utils import ContentInit, ToolInit
try:
    from Products.CMFCore import permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.DirectoryView import registerDirectory

# Archetypes imports
from Products.Archetypes.public import process_types, listTypes

# Products imports
from Products.PloneGlossary.config import SKINS_DIR, GLOBALS, PROJECTNAME
from Products.PloneGlossary.PloneGlossaryTool import PloneGlossaryTool
from Products.PloneGlossary.types import *
from Products.PloneGlossary import config

LOG = logging.getLogger('PloneGlossary')

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):

    # import at initialize: this let a chance to 3rd party products to change
    # config before deciding to patch
    import patches

    # used by test framework
    if config.DEBUG:
        import examples
        
    # Import types
    listOfTypes = listTypes(PROJECTNAME)
    content_types, constructors, ftis = process_types(listOfTypes,
                                                      PROJECTNAME)
    ContentInit('%s Content' % PROJECTNAME,
                content_types = content_types,
                permission = CMFCorePermissions.AddPortalContent,
                extra_constructors = constructors,
                fti = ftis,
                ).initialize(context)
    
    # Import tool
    ToolInit(
        '%s Tool' % PROJECTNAME,
        tools=(PloneGlossaryTool,),
        icon='tool.gif').initialize(context)
