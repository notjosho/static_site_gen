from htmlnode import HTMLNode


class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("ParentNode Tag is None")
    if self.children is None:
      raise ValueError("ParentNode children is None")
    html_join = ''.join([child.to_html() for child in self.children])
    if self.props is None:
      return f"<{self.tag}>{html_join}</{self.tag}>"
    return f"<{self.tag} {self.props}>{html_join}</{self.tag}>"
  