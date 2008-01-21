# -*- coding: utf-8 -*-
##
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
## along with this program; see the file LICENSE. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# $Id$
"""
Installation
"""

from Products.CMFCore.utils import getToolByName
from Products.PloneGlossary.config import INSTALL_EXAMPLES, UNITTESTS

def install(self, reinstall=False):
    """We need an install func because there are conditional installs"""

    tool=getToolByName(self, "portal_setup")

    tool.runAllImportStepsFromProfile(
        "profile-Products.PloneGlossary:ploneglossary",
        purge_old=False)

    if INSTALL_EXAMPLES:
        tool.runAllImportStepsFromProfile(
            "profile-Products.PloneGlossary:ploneglossary_examples",
            purge_old=False)

    return

