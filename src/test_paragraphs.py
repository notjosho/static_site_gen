import unittest

from helperfunctions import markdown_to_html_node

class TestParagraphs(unittest.TestCase):
  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    node = markdown_to_html_node(md)

    self.assertEqual(
        node,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    node = markdown_to_html_node(md)
    self.assertEqual(
        node,
        "<div><pre><code>This is text that _should_ remain the **same** even with inline stuff</code></pre></div>",
    )
  
  def unordered_ordered_list_inline_text(self):
    md = '''- Item 1
- Item 2 **bold**
- Item 3
- Item 4

1. Item 5
2. Item 6
3. Item 2
4. Item 7

Plain text paragraph here.

# Header one

# Header two

## Header three

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here'''
    node = markdown_to_html_node(md)
    self.assertEqual(
      node,
      "<div><ul><li>Item 1</li></ul><ol><li>Item 5</li></ol><p>Plain text paragraph here.</p><h1>Header one</h1><h1>Header two</h1><h2>Header three</h2><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )
