"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import re
import unicodedata
from sgmllib import SGMLParser

# Zope imports
from Globals import InitializeClass

END_NEWLINE_TAGS = ('p',)
START_NEWLINE_TAGS = ('br',)
TAB_TAGS = ('li',)
CHARS_TO_REMOVE = r'[\r\n]'
RE_CHARS_TO_REMOVE = re.compile(CHARS_TO_REMOVE)

class HTML2TextParser(SGMLParser):
    """HTML -> text
    """
      
    def __init__(self):
        SGMLParser.__init__(self)
        self.result = ''
    
    def handle_data(self, data):
        if len(data) > 0:
            data = RE_CHARS_TO_REMOVE.sub('', data)
            self.result += data
            
    def unknown_starttag(self, tag, attributes):
        if tag in START_NEWLINE_TAGS:
            self.result += '\n'
        
        if tag in TAB_TAGS:
            self.result += '\n - '
        
    def unknown_endtag(self, tag):
        if tag in END_NEWLINE_TAGS:
            self.result += '\n'

InitializeClass(HTML2TextParser)

MULTIPLE_SPACES = r' +'
RE_MULTIPLE_SPACES = re.compile(MULTIPLE_SPACES)
MULTIPLE_NEWLINES = r'\n+'
RE_MULTIPLE_NEWLINES = re.compile(MULTIPLE_NEWLINES)

def html2text(html):
    """Transform html to text"""
    
    output = html
    output = output.replace('\r',' ')
    output = output.replace('\n',' ')
    if len(output) > 0:
        parser = HTML2TextParser()
        parser.feed(output)
        parser.close()
        output = parser.result
        
        # Replace multiple spaces and newline by one
        output = RE_MULTIPLE_SPACES.sub(' ', output)
        output = RE_MULTIPLE_NEWLINES.sub('\n', output)
        
        # Strip chars
        output = output.strip()
    
    return output


SEARCH_WORDS = r'[\s:;.,\'\{\}\(\)\|]*'
RE_SEARCH_WORDS = re.compile(SEARCH_WORDS)

def text2words(text):
    """Extract all words from text"""
    
    words = []
    
    # Remove empty words and same words
    for word in RE_SEARCH_WORDS.split(text):
        if len(word) > 0 and word not in words:
            words.append(word)

    return tuple(words)

def encode(text, decoding=None, encoding=None):
    """Encode in specified encoding"""
    
    if encoding == decoding:
        return text
    
    if decoding is not None:
        text = text.decode(decoding, "replace")
    
    if encoding is not None and encoding != 'unicode':
        text = text.encode(encoding, "replace")
    
    return text

SEARCH_SPECIAL_CHARS = r'[\t\r\n\"\']'
RE_SEARCH_SPECIAL_CHARS = re.compile(SEARCH_SPECIAL_CHARS)

def escape_special_chars(text):
    """Quote text"""
    
    # Method to replace link by new one
    def escape(match):
        """Escape chars"""
        
        char = match.group(0)
        
        if char== '\n':
            return '\\n'
        elif char== '\r':
            return '\\n'
        elif char== '\t':
            return '\\t'
        
        
        return '\\%s' % char
    
    text = RE_SEARCH_SPECIAL_CHARS.sub(escape, text)
    return text

def encode_ascii(utext):
    """Normalize text : returns an ascii text
    
    @param utext: Unicode text to normalize"""
    
    # Ascii text of utext
    atext = ''
    
    for uchar in utext:
        # Normalize char
        nchar = unicodedata.normalize('NFKD', uchar)
        atext += nchar[0].encode('ascii', 'replace')
        
    atext = atext.lower()
    atext = atext.replace('?', ' ')
    return atext

def find_word(word, text):
    """Returns all found positions of the word in text.
    
    word and text parameters must use the same encoding
    
    @param word: word to search
    @param text: Text where you search the word"""
    
    # All found position
    found_pos = []
    
    # Search all positions
    index = 0 # First index where you search the word
    
    while 1:
        pos = text.find(word, index)
        if pos == -1:
            break
        found_pos.append(pos)
        index = pos + 1
    
    return tuple(found_pos)
