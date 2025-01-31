import unittest

from helperfunctions import separate_text_based_on_markdown
from textnode import TextNode, TextType

class TestSeparateTextBasedOnMarkDownFn(unittest.TestCase):
  def test_separate_text_based_on_markdown_all_delimiters(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    separated_nodes_based_on_markdown = separate_text_based_on_markdown(text)

    self.assertEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
      separated_nodes_based_on_markdown
    )

  def test_separate_text_based_on_markdown_some_delimiters(self):
    text = "This is **text** with a and a `code block` and a [link](https://boot.dev)"
    separated_nodes_based_on_markdown = separate_text_based_on_markdown(text)

    self.assertEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with a and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
      separated_nodes_based_on_markdown
    )

  def test_separate_text_based_on_markdown_some_delimiters_repeated(self):
    text = "This is *text* with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![boot dev image](https://boot.dev)"
    separated_nodes_based_on_markdown = separate_text_based_on_markdown(text)

    self.assertEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.ITALIC),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("boot dev image", TextType.IMAGE, "https://boot.dev"),
      ],
      separated_nodes_based_on_markdown
    )

  def test_separate_text_based_on_markdown_all_delimiters_not_applied(self):
    text = "This is text with an *italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg) and a link https://boot.dev)"
    separated_nodes_based_on_markdown = separate_text_based_on_markdown(text)
    
    self.assertEqual(
      [
        TextNode("This is text with an *italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg) and a link https://boot.dev)", TextType.TEXT),
      ],
      separated_nodes_based_on_markdown
    )

if __name__ == "__main__":
  unittest.main()