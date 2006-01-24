Dependencies
============

Required Products
------------------

* Plone 2.0.4 or 2.0.5 and Plone 2.1 and higher

* Archetypes >= 1.3.1

Installation
============
  
Installing PloneGlossary
------------------------

* Unpack it into your Zope Products Folder

* Restart Zope

* Use portal_quickinstaller to install the PloneGlossary in ZMI 
  (or use plone_setup in pmi)

* Now you can add a Plone Glossary through the Plone Interface. (Adding a Plone
  Glossary through the ZMI won't work).

Migration
---------

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

Overview
========
  
  PloneGlossary is a Plone content type that allows you to manage your own 
  glossaries, propose definitions and search in one or more glossaries. Any word 
  defined is instantly highlighted in the content of your site.

  Once a glossary is created, you can add your definitions to it. Definitions
  are a simple content type. Enter the word you want to define as the title, and
  the definition of the word in the text body. You can also specify variants
  of the word. For example if you define the word yoghurt, you may also want to
  allow the variants yogurt or yoghourt to be valid. Definitions will be 
  highlighted (like an acronym) when they appear elsewhere in your site. (Also
  see the ploneglossary configlet.)
  
  Once you have a large number of definitions in your glossary, you can browse
  the glossary by the means of an alphabetic index, or perform a search in the
  glossary. Each glossary has an integrated search engine, which is simply a
  ZCatalog.

    The Glossary Configlet:
    
      Glossary portlet: If switched on, a portlet listing all definitions found
      in the currently shown content.
      
      Highlight content: if this option is chosen, all defined words are 
      hightlighted in the chosen content types (see further).
      
      Description length : Choose the maximum length of the given definition in
      the highlights.
      
      Description ellipsis: Choose an ellipsis. It is used in the highlight
      when the defined term exceeds the description length.
      
      Not highlighted tags: Define the html tags in which definitions should 
      not be highlighted. Default: h1, a, input, textarea
      
      Allowed portal types: Select the portal types for which defined words are
      highlighted.
      
      General glossaries: Select glossaries used to check related terms of 
      content.
  
Known Problems
----------------

  Glossary Portlet needs to be present

    If you don't want to show the portlet with the glossary words, you can 
    select the option "Show glossary porlet ?", and the portlet will be hidden
    using CSS.

    Attention: It is still necessary to keep the portlet in the slot in any
    case, as it contains the JavaScript code necessary for highlighting words.

    So, if you really have to remove the portlet, you'll have to include the
    JavaScript somewhere else in a global template. The best place may be the 
    CMFPlone file header.pt.

    We'll probably use the JavaScript Registry of Plone 2.1 in the future.

Additional tools
----------------
  
  PloneGlossaryTool
    
    A tool is installed by the installer. It provides a few configuration 
    options so that you can customize and manage your glossaries.

