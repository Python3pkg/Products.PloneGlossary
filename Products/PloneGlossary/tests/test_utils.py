import unittest
from Products.PloneGlossary.utils import text2words


class UtilsTestCase(unittest.TestCase):

    def test_text2words(self):
        self.assertEqual(text2words('x'), ('x',))
        self.assertEqual(text2words('x Y'), ('x', 'Y'))
        self.assertEqual(text2words('foo bar'), ('foo', 'bar'))
        self.assertEqual(text2words('<p>foo bar</p>'), ('foo', 'bar'))
        self.assertEqual(text2words('foo<sub>bar</sub>'), ('foo', 'bar'))
        self.assertEqual(text2words('<p class="shiny">text</p>'), ('text',))
        self.assertEqual(text2words('<p \n>text</\np>'), ('text',))
        self.assertEqual(text2words('<br/>  <br />'), ())
