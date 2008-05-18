#############
PloneGlossary
#############

By Ingeniweb_.

--------------------------

.. contents:: **Table of contents**

--------------------------

Overview
########

PloneGlossary is a Plone content type that allows you to manage your
own glossaries, propose definitions and search in one or more
glossaries. Any word defined is instantly highlighted in the content
of your site.

After adding a glossary, you can add your definitions to
it. Definitions are a simple content type. Enter the word you want to
define as the title, and the definition of the word in the text
body. You can also specify variants of the word. For example if you
define the word yoghurt, you may also want to allow the variants
yogurt or yoghourt to be valid. Definitions will be highlighted (like
an acronym) when they appear elsewhere in your site. (Also see the
ploneglossary configlet.)

Once you have a large number of definitions in your glossary, you can
browse the glossary by the means of an alphabetic index, or perform a
search in the glossary. Each glossary has an integrated search engine,
which is simply a ZCatalog.


Copyright and license
#####################

Copyright (c) 2005 - 2007 Ingeniweb_ SAS

This software is subject to the provisions of the GNU General Public License,
Version 2.0 (GPL).  A copy of the GPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE

See the `LICENSE` file that comes with this product.

Requirements
############

Plone 3.0

Installation
############

Installing PloneGlossary
========================

* Unpack it into your Zope Products Folder

* Restart Zope

* Use portal_quickinstaller to install the PloneGlossary in ZMI
  (or use plone_setup in pmi)

* Now you can add a Plone Glossary through the Plone Interface. (Adding a Plone
  Glossary through the ZMI won't work).

Plone Unicode issue
===================

Due to an open issue in the Javascript registry tool, using non ASCII
characters in your glossary requires to change the default encoding of
your Zope. To do this, add a sitecustomize.py file to your
$SOFTWARE_HOME with these two lines::

  import sys
  sys.setdefaultencoding('utf-8')

Replace "utf-8" above with the value of the "default_charset" property
in your "portal_properties/site_properties".

More information `here <http://dev.plone.org/plone/ticket/7522>`_

Migration
=========

We provide a migration script for PloneGlossary 1.2 to 1.3. All the migration
does is add an index and a metadata to the catalogs inside the PloneGlossaries.

* In the ZMI, go to the portal_glossary tool

* Follow the instructions in the Migration Tab

When migrating you have 2 choices :

1- Specifying the meta_type of your glossaries. This is normally "PloneGlossary",
   and if you are in doubt, leave this field unchanged.
   People who inherited from PloneGlossary should enter the meta_types of their
   content type and run migrations individually.

2- In dry run mode, migration is done, it is only a simulation of a migration,
   allowing you to the log to see if everything is ok.


Configuring
###########

Add a glossary portlet
======================

Use the portlets manager to display a portlet of all definitions found
in the displayed content.

zope.conf tweaks (optional)
===========================

PloneGlossary assumes that your site charset is UTF-8. As this charset
must be known very early in Zope startup, we cannot always use the
charset in the properties of your Plone site.

PloneGlossary views have a batch size of 30 terms. You might prefer
another size.

If the Plone sites of your instance use another charset, or if you
need another batch size, you might append this to your `zope.conf`::

  <product-config ploneglossary>
    charset iso-8859-15 # Or any valid charset that suits your needs.
    batch-size 40 # Or any positive integer you might prefer.
  </product-config>


The Glossary configlet
======================

Highlight content: if this option is chosen, all defined words
are hightlighted in the chosen content types (see further).

Description length : Choose the maximum length of the given definition
in the highlights.

Description ellipsis: Choose an ellipsis. It is used in the highlight
when the defined term exceeds the description length.

Not highlighted tags: Define the html tags in which definitions should
not be highlighted. Default: h1, a, input, textarea

Allowed portal types: Select the portal types for which defined words
are highlighted.

Use glossaries globally for all content?: When checked, all glossaries
will be used to highlight terms globally for all of the site's
content. By unchecking this option, only the first glossary found
while traversing upwards from the content is used.

General glossaries: Select glossaries used to check related terms of
content.

Additional tools
================

PloneGlossaryTool
-----------------

A tool is installed by the installer. It provides a few configuration
options so that you can customize and manage your glossaries.


Testing
#######

Please read `./tests/README.txt`.


Other documentation
###################

See `./doc`.


Downloads
#########

You may find newer stable versions of FSS and pointers to related
informations (tracker, doc, ...) from
http://plone.org/products/ploneglossary


Subversion repository
#####################

Stay in tune with the freshest (maybe unstable) versions or participate to
the FileSystemStorage evolutions:

https://svn.plone.org/svn/collective/PloneGlossary

Support and feedback
####################

Please read all the documentation that comes with this product before
asking for support, unless you might get a RTFM reply ;)

Localisation issues - other than french - should be reported to the
relevant translators (see Credits_ below).

Report bugs using the tracker (the `Tracker` link from
http://plone.org/products/ploneglossary). Please provide in your
bug report:

* Your configuration (Operating system+Zope+Plone+Products/versions).
* The full traceback if available.
* One or more scenario that triggers the bug.

Note that we do not support bug reports on Subversion trunk or
branches checkouts.

`Mail to Ingeniweb support <mailto:support@ingeniweb.com>`_ in English or
French to ask for specific support.

`Donations are welcome for new features requests
<http://sourceforge.net/project/project_donations.php?group_id=74634>`_

Credits
#######

Developers
==========

* `Cyrille Lebeaupin <mailto:cyrille.lebeaupin@ingeniweb.com>`_
* `Bertrand Mathieu <mailto:bertrand.mathieu@ingeniweb.com>`_
* `Maik Roeder <mailto:maik.roeder@ingeniweb.com>`_
* `Gilles Lenfant <mailto:gilles.lenfant@ingeniweb.com>`_

Translations
============

* French (fr): Ingeniweb_
* Czech (cs): `Lukas Zdych <mailto:lukas.zdych@corenet.cz>`_
* Danish (da): `Anton Stonor <mailto:anton@headnet.dk>`_
* German (de): `Lukas Zdych <mailto:lukas.zdych@corenet.cz>`_
* Polish (pl): `Piotr Furman <mailto:piotr.furman@webservice.pl>`_
* Spanish (es): `Héctor Velarde <mailto:hvelarde@jornada.com.mx>`_

--------------------------

.. sectnum::
.. _Ingeniweb: http://www.ingeniweb.com/
.. _PloneGlossary: http://plone.org/products/ploneglossary
.. $Id$
