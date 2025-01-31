import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
  def test_parent_node_props(self):
    node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ],
    )
    self.assertEqual(
      node.to_html(),
      '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
    )

  def test_empty_children(self):
    node = ParentNode(
      "p", []
    )
    self.assertEqual(
      node.to_html(),
      '<p></p>'
    )

  def test_nested_parent_nodes(self):
    inner_parent_node = ParentNode(
      "div",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
      ])
    node = ParentNode(
      "div",
      [
        inner_parent_node,
      ]
    )
    self.assertEqual(
      node.to_html(),
      '<div><div><b>Bold text</b>Normal text</div></div>'
    )

  def test_invalid_tag_values(self):
    with self.assertRaises(ValueError) as context:
      node = ParentNode(
        None,
        [
          LeafNode(None, "Text")
        ]
      )
      node.to_html()

    self.assertEqual(
      str(context.exception),
      'ParentNode Tag is None'
    )

  def test_no_children_argument(self):
    with self.assertRaises(TypeError) as context:
      node = ParentNode(
        "div"
      )
      node.to_html()

    self.assertEqual(
      str(context.exception),
      "ParentNode.__init__() missing 1 required positional argument: 'children'"
    )

  def test_combination_parent_and_leaf_nodes(self):
    inner_parent_node = ParentNode(
      "div",
      [
        LeafNode("i", "italic"),
        LeafNode(None, "text")
      ]
    )
    node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        inner_parent_node,
        LeafNode(None, "Normal text"),
      ],
    )
    self.assertEqual(
      node.to_html(),
      '<p><b>Bold text</b>Normal text<i>italic text</i><div><i>italic</i>text</div>Normal text</p>'
    )

  def test_grand_child_node(self):
    grand_child_node = ParentNode(
      "div",
      [
        LeafNode("i", "italic"),
        LeafNode(None, "text")
      ]
    )
    parent_node = ParentNode(
      "div",
      [
        LeafNode("b", "bold text"),
        LeafNode(None, "text"),
        grand_child_node
      ]
    )
    node = ParentNode(
      "h1",
      [
        LeafNode(None, "Something"),
        parent_node
      ]
    )
    self.assertEqual(
      node.to_html(),
      '<h1>Something<div><b>bold text</b>text<div><i>italic</i>text</div></div></h1>'
    )


if __name__ == "__main__":
  unittest.main()