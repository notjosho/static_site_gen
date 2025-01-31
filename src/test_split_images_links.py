import unittest

from helperfunctions import split_nodes_images, split_nodes_link
from textnode import TextNode, TextType

class TestSplitImagesLinks(unittest.TestCase):
  def test_split_links(self):
    node_new_links = TextNode(
      "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes_link = split_nodes_link([node_new_links])
    expected_string = ""
    for i in new_nodes_link:
      expected_string += f"{i.__repr__()}, "
    expected_string = expected_string[:-2]
    self.assertEqual(
      f"[{expected_string}]",
      '[TextNode("This is text with a link ", "text"), TextNode("to boot dev", "links", "https://www.boot.dev"), TextNode(" and ", "text"), TextNode("to youtube", "links", "https://www.youtube.com/@bootdotdev")]'
    )

  def test_split_images(self):
    node_new_images = TextNode(
      "This is text with a link ![boot dev image](https://www.boot.dev) and ![youtube image](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
  
    new_nodes_images = split_nodes_images([node_new_images])
    expected_string = ""
    for i in new_nodes_images:
      expected_string += f"{i.__repr__()}, "
    expected_string = expected_string[:-2]
    
    self.assertEqual(
      f"[{expected_string}]",
      '[TextNode("This is text with a link ", "text"), TextNode("boot dev image", "images", "https://www.boot.dev"), TextNode(" and ", "text"), TextNode("youtube image", "images", "https://www.youtube.com/@bootdotdev")]'
    )

  def test_no_split_links(self):
    node_new_links = TextNode(
      "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes_link = split_nodes_link([node_new_links])
    
    expected_string = ""
    for i in new_nodes_link:
      expected_string += f"{i.__repr__()}, "
    expected_string = expected_string[:-2]

    self.assertEqual(
      f"[{expected_string}]",
      '[TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", "text")]'
    )
 

  def test_no_split_images(self):
    node_new_images = TextNode(
      "This is text with a link [boot dev image](https://www.boot.dev) and [youtube image](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes_images = split_nodes_images([node_new_images])
    expected_string = ""
    for i in new_nodes_images:
      expected_string += f"{i.__repr__()}, "
    expected_string = expected_string[:-2]
    
    self.assertEqual(
      f"[{expected_string}]",
      '[TextNode("This is text with a link [boot dev image](https://www.boot.dev) and [youtube image](https://www.youtube.com/@bootdotdev)", "text")]'
    )



if __name__ == "__main__":
  unittest.main()
