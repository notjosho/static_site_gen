import unittest

from helperfunctions import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
  def test_extract_markdown_images(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    self.assertEqual(
      extract_markdown_images(text),
      [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    )

  def test_extract_markdown_links(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

    self.assertEqual(
        extract_markdown_links(text),
        [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    )

  def test_extract_markdown_images_no_matches(self):
    text = "This is text with a ![rick roll]https://i.imgur.com/aKaOqIh.gif) and obi wan(https://i.imgur.com/fJRm4Vk.jpeg)"

    self.assertEqual(
      extract_markdown_images(text),
      []
    )

  def test_extract_markdown_links_no_matches(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev"
    
    self.assertEqual(
      extract_markdown_links(text),
      []
    )
     

if __name__ == "__main__":
  unittest.main()
