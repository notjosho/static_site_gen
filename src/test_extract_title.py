import textwrap
import unittest

from helperfunctions import extract_title

class TestExtractTitle(unittest.TestCase):
  def test_happy_path(self):
    text = textwrap.dedent('''
    # Some Title

    Some other text
    some other text 2
                                    
    - a list item 1
    - a list item 2
    - a list item 3
    ''')

    self.assertEqual(extract_title(text), 'Some Title')

  def test_spaces_in_title(self):
    text = textwrap.dedent('''
    # Some Title Spaces     

    Some other text
    some other text 2
                                    
    - a list item 1
    - a list item 2
    - a list item 3
    ''')
    print(f"---------->extract_title(text): _{extract_title(text)}_")

    self.assertEqual(extract_title(text), 'Some Title Spaces')

  def test_no_title_found(self):
    text = textwrap.dedent('''
    Some title 

    - Some text
    - Some text 2
                            
    Some text 3                       
    Some text 4                        
    ''')


    self.assertEqual(extract_title(text), '')