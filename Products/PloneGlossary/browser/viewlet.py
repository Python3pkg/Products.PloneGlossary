# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets import ViewletBase


class DefinitionViewlet(ViewletBase):
    """Render the ploneglossary_definitions js in a viewlet."""

    render = ViewPageTemplateFile('./ploneglossary_script.pt')
