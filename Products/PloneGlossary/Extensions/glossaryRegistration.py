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


from Products.CMFCore.utils import getToolByName
from Products.PloneGlossary.config import PLONEGLOSSARY_TOOL

def registerGlossary(context, glossaryClass, out):
    pgtool = getToolByName(context, PLONEGLOSSARY_TOOL)
    registered_metatypes = pgtool.available_glossary_metatypes
    new_glossary_metatype = glossaryClass.meta_type
    if not new_glossary_metatype in registered_metatypes:
        pgtool.available_glossary_metatypes += (new_glossary_metatype,)
        out.write("%s glossary registered" % new_glossary_metatype)