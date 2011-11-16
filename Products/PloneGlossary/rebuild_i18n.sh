#!/bin/bash
# Run this script to update the translations.

# Rebuild the pot file for the ploneglossary domain.
i18ndude rebuild-pot --pot i18n/glossary.pot --create ploneglossary .
# Sync with the ploneglossary po files.
i18ndude sync --pot i18n/glossary.pot $(find i18n -iregex '.*\.po$'|grep -v plone)
