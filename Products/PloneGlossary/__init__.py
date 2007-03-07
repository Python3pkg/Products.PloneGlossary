"""
$Id$
"""
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import sys
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

import patches

if config.DEBUG:
    import examples

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
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
