class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("to_html method not implemented")
  
  def props_to_html(self):
    if self.props is None:
      return ""
    props_string = ""
    for key in self.props:
      props_string += f'{key}="{self.props[key]}" '
    return props_string.strip()

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

  def __eq__(self, node):
    if not isinstance(node, HTMLNode):
      return False
    return self.__repr__() == node.__repr__()
  