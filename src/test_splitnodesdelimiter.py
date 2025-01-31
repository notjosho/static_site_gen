import unittest

from helperfunctions import single_split_node_delimiter, split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_nodes_delimiter_happy_paths(self):
    node = TextNode("This is text with a **bold block** word", TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    node_code = TextNode("This is text with a word `code block`", TextType.TEXT)
    new_code_nodes = split_nodes_delimiter([node_code], "`", TextType.CODE)
    node_first = TextNode("*code block* This is a text with a word", TextType.TEXT)
    new_nodes_italic = split_nodes_delimiter([node_first], "*", TextType.ITALIC)
    
    test_bold_nodes = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("bold block", TextType.BOLD),
      TextNode(" word", TextType.TEXT),
    ]

    test_code_nodes = [
      TextNode("This is text with a word ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
    ]

    test_italic_nodes = [
      TextNode("code block", TextType.ITALIC),
      TextNode(" This is a text with a word", TextType.TEXT),
    ]

    for i, node in enumerate(bold_nodes):
      self.assertEqual(
        bold_nodes[i],
        test_bold_nodes[i]
      )

    for i in range(2):
      self.assertEqual(
        new_code_nodes[i],
        test_code_nodes[i]
      )

      self.assertEqual(
        new_nodes_italic[i],
        test_italic_nodes[i]
      )


  def test_single_node_delimiter_value_error(self):
    with self.assertRaises(ValueError) as context:
      node_first_non = TextNode("`code block This is text with a word", TextType.TEXT)
      new_nodes_first_non = single_split_node_delimiter(node_first_non, "`", TextType.CODE)

    self.assertIn(
      f"Invalid syntax, no closer delimiter found: {"`"}",
      str(context.exception)
    )

  def test_nodes_delimiter_more_than_one_match(self):
    node = TextNode("This is text with a **bold block** word **bold block2** word2 **bold block 3**", TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    test_bold_nodes = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("bold block", TextType.BOLD),
      TextNode(" word ", TextType.TEXT),
      TextNode("bold block2", TextType.BOLD),
      TextNode(" word2 ", TextType.TEXT),
      TextNode("bold block 3", TextType.BOLD),
    ]

    self.assertEqual(
      bold_nodes,
      test_bold_nodes
    )

  def test_nodes_delimiter_italic_more_than_one_match(self):
    node = TextNode("This is text with a *italics block* word *italics block2* word2", TextType.TEXT)
    italics_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

    test_italics_nodes = [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("italics block", TextType.ITALIC),
      TextNode(" word ", TextType.TEXT),
      TextNode("italics block2", TextType.ITALIC),
      TextNode(" word2", TextType.TEXT),
    ]

    self.assertEqual(
      italics_nodes,
      test_italics_nodes
    )
  
  def test_nodes_delimiter_italic_no_matches(self):
    node = [TextNode("This is text with a *italics block word italics block2 word2", TextType.TEXT)]
    italics_nodes = split_nodes_delimiter(node, "*", TextType.ITALIC)

    self.assertEqual(
      italics_nodes,
      node
    )


if __name__ == '__main__':
  unittest.main()
