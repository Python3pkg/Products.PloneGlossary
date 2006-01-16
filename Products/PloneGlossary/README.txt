Dependencies
============

Required Products
------------------

* Plone 2.0.4 or more
* Archetypes >= 1.3.1

  
Installation
============
  
Installing PloneGlossary
------------------------

* Unpack it into your Zope Products Folder
* Restart Zope
* Use portal_quickinstaller to install the PloneGlossary in ZMI (or use plone_setup in pmi)
* Now you can add a Plone Glossary through the Plone Interface. (Adding a Plone Glossary through the ZMI won't work).
  

Overview
========
  
  PloneGlossary is a Plone content type that allows you to manage your own 
  glossary, propose definitions and search in one or more glossary. Any word 
  defined is instantly highlight in your site whereever it apears.

  Once a glossary is created, you can add your definitions to it. 
  Definitions are a simple content type. Enter the word you want to define as the 
  title and the definition of the word in the text body.
  Definitions will be highlighted (like an acronym) when they appear elsewhere in your 
  site. (see the ploneglossary configlet)
  
  Once you have a large number of definitions in your glossary, you can browse the
  glossary by the means of an alphabetic index, or perform a search with the 
  integrated search engine.
  
    
    Manage your Glossary
    
      Glossary portlet: a portlet listing all definitions found in the currently 
      shown content.
      
      Highlight content: if this option is chosen, all defined words are hightlighted
      in the chosen content types (see further).
      
      Description length : Choose the maximum length of the given definition in
      the highlights.
      
      Description ellipsis: Choose an ellipsis. It is used in the highlight
      when the defined term exceeds the description length.
      
      Not highlighted tags: Define the html tags in which definitions should 
      not be highlighted. Default: h1, a, input, textarea
      
      Allowed portal types: Select the portal types for which defined words are highlighted.
      
      General glossaries: Select glossaries used to check related terms of 
      content.
  
Known Problems
----------------

  Glossary Portlet needs to be present

    If you don't want to show the portlet with the glossary words, you can select
    the option "Show glossary porlet ?", and the portlet will be hidden using CSS.

    Attention: It is still necessary to keep the portlet in the slot in any case, 
    as it contains the JavaScript code necessary for highlighting words.

    So, if you really have to remove the portlet, you'll have to include the JavaScript
    somewhere else in a global template. The best place may be the CMFPlone file 
    header.pt.

    Once the product is prepared for Plone 2.1 we'll probably use the JavaScript Registry.


Additional tools
----------------
  
  PloneGlossaryTool
    
    A tool is installed by the installer. It provides a few configuration 
    options so that you can customize and manage your glossaries.

