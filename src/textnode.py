from enum import Enum

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "links"
  IMAGE = "images"

class TextNode:
  def __init__(self, text: str, text_type: TextType, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, text_node):
    return self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url 

  def __repr__(self):
    url = f'"{self.url}"' if self.url else None
    if self.text_type == TextType.TEXT:
      return f'TextNode("{self.text}", "{self.text_type.value}")'
    return f'TextNode("{self.text}", "{self.text_type.value}", {url})'
  
class TextTypeMarkdown(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"
