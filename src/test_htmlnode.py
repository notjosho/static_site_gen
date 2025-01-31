import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_to_html_props(self):
    node = HTMLNode(
      "div",
      "Hello, world!",
      None,
      {"class": "greeting", "href": "https://boot.dev"},
    )
    self.assertEqual(
      node.props_to_html(),
      'class="greeting" href="https://boot.dev"',
    )

  def test_2_nodes_equal(self):
    node_first = HTMLNode(
      "div",
      "Something",
      None,
      {"class": "something", "href": "https://boot.dev"}
    )
    node_second = HTMLNode(
      "div",
      "Something",
      None,
      {"class": "something", "href": "https://boot.dev"}
    )
    self.assertEqual(
      node_first, node_second
    )

  def test_values(self):
    node = HTMLNode(
      "div",
      "Something",
    )

    self.assertEqual(node.tag, "div")
    self.assertEqual(node.value, "Something")
    self.assertEqual(node.children, None)
    self.assertEqual(node.props, None)
   
  def test_repr(self):
    node = HTMLNode(
      "h1",
      "Title",
      None,
      {"class": "title_case", "href": "https://boot.dev"}
    )

    self.assertEqual(node.__repr__(),f"HTMLNode({node.tag}, {node.value}, children: {node.children}, {node.props})")
    print(node.__repr__())
    self.assertEqual(node.__repr__(), "HTMLNode(h1, Title, children: None, {'class': 'title_case', 'href': 'https://boot.dev'})")


if __name__ == "__main__":
  unittest.main()
