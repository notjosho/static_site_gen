import unittest

from helperfunctions import text_node_to_html_node
from textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):
  def test_simple_types(self):
    text_node_default = "This is a text node"
    text_node_normal = TextNode(text_node_default, TextType.TEXT)
    html_node_normal = text_node_to_html_node(text_node_normal)
    self.assertEqual(html_node_normal.tag, "p")
    self.assertEqual(html_node_normal.value, text_node_normal.text)
    self.assertEqual(html_node_normal.props, None)
    self.assertEqual(html_node_normal.children, None)

    text_node_bold = TextNode(text_node_default, TextType.BOLD)
    html_node_bold = text_node_to_html_node(text_node_bold)
    self.assertEqual(html_node_bold.value, text_node_bold.text)
    self.assertEqual(html_node_bold.tag, "b")
    self.assertEqual(html_node_bold.props, None)
    self.assertEqual(html_node_bold.children, None)

    text_node_italic = TextNode(text_node_default, TextType.ITALIC)
    html_node_italic = text_node_to_html_node(text_node_italic)
    self.assertEqual(html_node_italic.value, text_node_italic.text)
    self.assertEqual(html_node_italic.tag, "i")
    self.assertEqual(html_node_italic.props, None)
    self.assertEqual(html_node_italic.children, None)

    text_node_code = TextNode(text_node_default, TextType.CODE)
    html_node_code = text_node_to_html_node(text_node_code)
    self.assertEqual(html_node_code.value, text_node_code.text)
    self.assertEqual(html_node_code.tag, "code")
    self.assertEqual(html_node_code.props, None)
    self.assertEqual(html_node_code.children, None)
    
  def test_node_props_types(self):
    text_node_default = "Node props types, url text"
    url = "https://joshhu.com"
    text_node_links = TextNode(text_node_default, TextType.LINK, url)
    html_node_links = text_node_to_html_node(text_node_links)
    self.assertEqual(html_node_links.value, text_node_links.text)
    self.assertEqual(html_node_links.tag, "a")
    self.assertEqual(html_node_links.props,  {"href": text_node_links.url})
    self.assertEqual(html_node_links.children, None)

    text_node_images = TextNode(text_node_default, TextType.IMAGE, url)
    html_node_images = text_node_to_html_node(text_node_images)
    self.assertEqual(html_node_images.value, text_node_images.text)
    self.assertEqual(html_node_images.tag, "img")
    self.assertEqual(html_node_images.props, {"src": text_node_images.url, "alt": text_node_images.text})
    self.assertEqual(html_node_images.children, None)

  def test_node_type_error(self):
    text_node_default = "Type Error text"
    with self.assertRaises(ValueError) as context:
      text_node = TextNode(text_node_default, "h1")
      html_node = text_node_to_html_node(text_node)

    self.assertEqual(
      str(context.exception),
      "Invalid text type: h1"
    )

if __name__ == '__main__':
  unittest.main()
