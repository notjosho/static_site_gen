import unittest

from helperfunctions import markdown_to_blocks
from helper_vars import markdown

class MarkDownToBlocks(unittest.TestCase):
  def test_markdown_to_blocks(self):
    markdown_blocks = markdown_to_blocks(markdown)
    test_markdown_blocks = [
      ['# This is a heading'],
      ['This is a paragraph of text. It has some **bold** and *italic* words inside of it.'],
      ['* This is the first list item in a list block',
        '* This is a list item',
        '* This is another list item']]
    
    self.assertEqual(
      markdown_blocks, 
      test_markdown_blocks
    )

  def test_markdown_to_blocks_one_line(self):
    markdown_blocks = markdown_to_blocks('# This is a heading 2')
    test_markdown_blocks = [['# This is a heading 2']]
    
    self.assertEqual(
      markdown_blocks,
      test_markdown_blocks
    )

  def test_markdown_to_blocks_negative(self):
    markdown_blocks = markdown_to_blocks('')
    test_markdown_blocks = [[]]

    self.assertEqual(
      markdown_blocks,
      test_markdown_blocks
    )


if __name__ == "__main__":
  unittest.main()
