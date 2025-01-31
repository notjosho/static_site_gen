import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_text_type_not_equal(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.TEXT)
    self.assertNotEqual(node, node2)
  
  def test_text_not_equal(self):
    node = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is a text node 2", TextType.TEXT)
    self.assertNotEqual(node, node2)
  
  def test_empty_url_not_equal(self):
    node = TextNode("This is a text node", TextType.TEXT, "https://boot.dev")
    node2 = TextNode("This is a text node", TextType.TEXT)
    self.assertNotEqual(node, node2)

  def test_different_url_not_equal(self):
    node = TextNode("This is a text node", TextType.TEXT, "https://boot.dev")
    node2 = TextNode("This is a text node", TextType.TEXT, "https://boot1234.dev")
    self.assertNotEqual(node, node2)

  def test_same_url_equal(self):
    node = TextNode("This is a text node", TextType.TEXT, "https://boot.dev")
    node2 = TextNode("This is a text node", TextType.TEXT, "https://boot.dev")
    self.assertEqual(node, node2)



if __name__ == "__main__":
  unittest.main()
