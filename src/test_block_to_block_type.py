import unittest

from helperfunctions import block_to_block_type
from textnode import TextTypeMarkdown


class TestBlockToBlockType(unittest.TestCase):
  def test_all_happy_paths(self):
    text_list = ['asdf', 
                 '```def function():```\n```  pass```', 
                 '> something\n> something2\n> something3', 
                 '* asdf\n* asdf2\n* asdf3', 
                 '- asdf\n- asdf2\n- asdf3',
                 '- asdf\n* asdf2\n* asdf3\n- some',
                 '1. asdf\n2. asdf2\n3. asdf 3\n4. asdf 4']

    expected_types = [TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.CODE, 
                      TextTypeMarkdown.QUOTE, 
                      TextTypeMarkdown.UNORDERED_LIST_ITEM, 
                      TextTypeMarkdown.UNORDERED_LIST_ITEM, 
                      TextTypeMarkdown.UNORDERED_LIST_ITEM, 
                      TextTypeMarkdown.ORDERED_LIST_ITEM]

    for i in range(len(text_list)):
      [type, value] = block_to_block_type(text_list[i])
      self.assertEqual(
        type, expected_types[i]
      )

  def test_all_paragraphs(self):
    text_list = ['asdf', '``def function():``` \n```  pass```', 
                 ' something\n> something2\n> something3', 
                 ' asdf\n* asdf2\n* asdf3', 
                 ' asdf\n- asdf2\n- asdf3',
                 ' asdf\n* asdf2\n* asdf3\n- some',
                 '1. asdf\n2. asdf2\n. asdf 3\n4. asdf 4',
                 '1. asdf\n4. asdf2\n3. asdf 3\n4. asdf 4']

    expected_types = [TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH]

    for i in range(len(text_list)):
      [type, value] = block_to_block_type(text_list[i])
      self.assertEqual(
        type, expected_types[i]
      )

  def test_paragraphs_markdown_symbols_in_the_middle_of_the_string(self):
    text_list = ['asdf', 
                 'asdf```def function():``` \n```  pass```', 
                 '> something\n > something2\n> something3', 
                 '* asdf\n * asdf2\n* asdf3', 
                 '- asdf\nasdf2 - \n- asdf3',
                 '- asdf\n * asdf2\n* asdf3\n- some',
                 '1. asdf\n 2. asdf2\n3. asdf 3\n4. asdf 4']

    expected_types = [TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH, 
                      TextTypeMarkdown.PARAGRAPH]


    for i in range(len(text_list)):
      [type, value] = block_to_block_type(text_list[i])
      self.assertEqual(
        type, expected_types[i]
      )

if __name__ == '__main__':
  unittest.main()

