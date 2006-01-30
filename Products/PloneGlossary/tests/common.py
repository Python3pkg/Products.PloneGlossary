"""
$Id$
"""

# Python imports
import os
import sys
from types import StringType

# Zope imports
from Testing import ZopeTestCase
from AccessControl import Unauthorized
from AccessControl import getSecurityManager

# CMF imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.interfaces.base import IBaseUnit

# Products imports
from Products.PloneGlossary.tests import PloneGlossaryTestCase
from Products.PloneGlossary.utils import find_word, encode_ascii

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
